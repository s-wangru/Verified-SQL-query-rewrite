import duckdb
import argparse
import subprocess
import os
import shutil
from enum import Enum

class Output(Enum):
    EQUAL = 0
    NEQUAL = 1
    INCONCLUSIVE = 2

def load_schema_and_data(schema_path, load_path):
    conn = duckdb.connect(database=':memory:')
    with open(schema_path, 'r') as f:
        schema = f.read()
        conn.execute(schema)
        conn.commit()

    with open(load_path, 'r') as f:
        sql = f.read()
        conn.execute(sql)
        conn.commit()
    
    return conn, schema

def qed(schema, orig, optimized):
    with open('tmp/temp.sql', 'w') as f:
        f.write(schema)
        f.write(orig)
        f.write(optimized)

    # nix run github:qed-solver/parser -- tests
    cmd = ["nix", "run", "github:qed-solver/parser", "--", "../tmp"]
    subprocess.run(cmd, cwd="parser/", capture_output=False, stderr=subprocess.DEVNULL)

    # nix run github:qed-solver/prover -- tests
    cmd = ["nix", "run", "github:qed-solver/prover", "--", "../tmp"]
    result = subprocess.run(cmd,  cwd="parser/", capture_output=True, text=True)

    lines = result.stdout.splitlines()
    output = False
    for line in lines:
        if "for temp.json" in line:
            if "not provable" in line:
                qed_output = Output.NEQUAL
            elif "provable" in line:
                qed_output = Output.EQUAL
            print("QED: " + line[:-13])
            output = True
            break

    if not output:
        qed_output = Output.INCONCLUSIVE
        print("QED: Cannot be determined")

    os.remove('tmp/temp.sql')
    return qed_output

def synthetic_data(conn, orig, optimized):
    df_orig = conn.execute(orig).fetchdf()
    try:
        df_optim = conn.execute(optimized).fetchdf()

        if df_orig.equals(df_optim):
            synthetic_output = Output.EQUAL
            print("Synthetic Data: The query results are equal")
        else:
            synthetic_output = Output.NEQUAL
            print("Synthetic Data: The query results are not equal")
    except Exception as e:
        synthetic_output = Output.INCONCLUSIVE
        print("Synthetic Data: Optimized query is not supported in DuckDB")

    return synthetic_output

if __name__ == "__main__":
    # prompt users for workload path, schema path, and load path
    parser = argparse.ArgumentParser(description="Test generated data on query pairs")
    parser.add_argument("--workload_path", type=str)
    parser.add_argument("--schema_path", type=str, default=None)
    parser.add_argument("--load_path", type=str, default=None)
    args = parser.parse_args()

    # load schema and table data
    conn, schema = load_schema_and_data(args.schema_path, args.load_path)

    qed_equals = 0
    qed_nequals = 0
    qed_cannotdet = 0

    equals = 0
    nequals = 0
    errors = 0

    agrees = 0
    disagrees = 0

    # make a temp directory
    os.makedirs('tmp', exist_ok=True)

    print("=========================================")

    with open(args.workload_path, 'r') as f:
        queries = f.read()
        queries = queries.split('User Query: ')[1:]

        for q in queries:
            qs = q.split('Optimized Query: ')
            if len(qs) < 2:
                print("Invalid query pair, skipping...")
                print("=========================================")
                continue

            orig = qs[0].strip()
            optimized = qs[1].strip()

            print("Query: " + orig[:30] + " ...")
            print("")

            qed_output = None
            synthetic_output = None

            # --------------------------------
            # ---------- QED STAGE -----------
            # --------------------------------

            qed_output = qed(schema, orig, optimized)
            if qed_output == Output.EQUAL:
                qed_equals += 1
            elif qed_output == Output.NEQUAL:
                qed_nequals += 1
            else:
                qed_cannotdet += 1

            # --------------------------------
            # ----- SYNTHETIC DATA STAGE -----
            # --------------------------------

            synthetic_output = synthetic_data(conn, orig, optimized)
            if synthetic_output == Output.EQUAL:
                equals += 1
            elif synthetic_output == Output.NEQUAL:
                nequals += 1
            else:
                errors += 1

            # --------------------------------

            if qed_output == synthetic_output:
                agrees += 1
            else:
                disagrees += 1

            print("=========================================")

    shutil.rmtree('tmp')

    print("")
    print("================SUMMARY==================")
    print(f"Total valid queries:                {equals + nequals + errors}")
    print("")
    print(f"QED - Equals:                       {qed_equals}")
    print(f"QED - Not Equals:                   {qed_nequals}")
    print(f"QED - Cannot Be Determined:         {qed_cannotdet}")
    print("")
    print(f"Synthetic Data - Equals:            {equals}")
    print(f"Synthetic Data - Not Equals:        {nequals}")
    print(f"Synthetic Data - Errors:            {errors}")
    print("")
    print(f"QED + Synthetic Stages Agree:       {agrees}")
    print(f"QED + Synthetic Stages Disagree:    {disagrees}")
    print("")