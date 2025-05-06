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

def qed(schema, orig, optimized, qed_equal_queries, qed_nequal_queries, qed_cannotdet_queries):
    os.makedirs('tmp', exist_ok=True)
    with open('tmp/temp.sql', 'w') as f:
        f.write(schema)
        f.write(orig)
        f.write("\n")
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
                qed_nequal_queries.append(orig)
            elif "provable" in line:
                qed_output = Output.EQUAL
                qed_equal_queries.append(orig)
            print("QED: " + line[:-13])
            output = True
            break

    if not output:
        qed_output = Output.INCONCLUSIVE
        qed_cannotdet_queries.append(orig)
        print("QED: Cannot be determined")

    os.remove('tmp/temp.sql')
    return qed_output

def synthetic_data(conn, orig, optimized, synthetic_equal_queries, synthetic_nequal_queries, synthetic_error_queries):
    try:
        df_orig = conn.execute(orig).fetchdf()
        df_optim = conn.execute(optimized).fetchdf()
        df_orig_sorted = df_orig.sort_values(by=df_orig.columns.tolist()).reset_index(drop=True)
        df_optim_sorted = df_optim.sort_values(by=df_optim.columns.tolist()).reset_index(drop=True)

        if df_orig_sorted.equals(df_optim_sorted):
            synthetic_output = Output.EQUAL
            synthetic_equal_queries.append(orig)
            print("Synthetic Data: The query results are equal")
        else:
            synthetic_output = Output.NEQUAL
            synthetic_nequal_queries.append(orig)
            print("Synthetic Data: The query results are not equal")
    except Exception as e:
        synthetic_output = Output.INCONCLUSIVE
        synthetic_error_queries.append(orig)
        print("Synthetic Data: Optimized query is not supported in DuckDB")

    return synthetic_output

if __name__ == "__main__":
    # prompt users for workload path, schema path, and load path
    parser = argparse.ArgumentParser(description="Test generated data on query pairs")
    parser.add_argument("--workload_path", type=str)
    parser.add_argument("--schema_path", type=str, default=None)
    parser.add_argument("--load_path", type=str, default=None)
    parser.add_argument("--output_path", type=str, default=None)
    args = parser.parse_args()

    qed_equal_queries = []
    qed_nequal_queries = []
    qed_cannotdet_queries = []
    synthetic_equal_queries = []
    synthetic_nequal_queries = []
    synthetic_error_queries = []

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

            qed_output = qed(schema, orig, optimized, qed_equal_queries, qed_nequal_queries, qed_cannotdet_queries)
            if qed_output == Output.EQUAL:
                qed_equals += 1
            elif qed_output == Output.NEQUAL:
                qed_nequals += 1
            else:
                qed_cannotdet += 1

            # --------------------------------
            # ----- SYNTHETIC DATA STAGE -----
            # --------------------------------

            synthetic_output = synthetic_data(conn, orig, optimized, synthetic_equal_queries, synthetic_nequal_queries, synthetic_error_queries)
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

    if args.output_path is not None:
        with open(args.output_path, 'w') as f:
            f.write(f"Total valid queries:                {equals + nequals + errors}\n")
            f.write(f"QED - Equals:                       {qed_equals}\n")
            f.write(f"QED - Not Equals:                   {qed_nequals}\n")
            f.write(f"QED - Cannot Be Determined:         {qed_cannotdet}\n")
            f.write(f"Synthetic Data - Equals:            {equals}\n")
            f.write(f"Synthetic Data - Not Equals:        {nequals}\n")
            f.write(f"Synthetic Data - Errors:            {errors}\n")
            f.write(f"QED + Synthetic Stages Agree:       {agrees}\n")
            f.write(f"QED + Synthetic Stages Disagree:    {disagrees}\n")

            f.write(f"--------------------------------------\n")
            f.write(f"QED Equal Queries:                  {len(qed_equal_queries)}\n")
            for query in qed_equal_queries:
                f.write(f"  Query: {query}\n")
            f.write(f"--------------------------------------\n")
            f.write(f"QED Not Equal Queries:              {len(qed_nequal_queries)}\n")
            for query in qed_nequal_queries:
                f.write(f"  Query: {query}\n")
            f.write(f"--------------------------------------\n")
            f.write(f"QED Cannot Determine Queries:       {len(qed_cannotdet_queries)}\n")
            for query in qed_cannotdet_queries:
                f.write(f"  Query: {query}\n")
            f.write(f"--------------------------------------\n")
            f.write(f"Synthetic Equal Queries:            {len(synthetic_equal_queries)}\n")
            for query in synthetic_equal_queries:
                f.write(f"  Query: {query}\n")
            f.write(f"--------------------------------------\n")
            f.write(f"Synthetic Not Equal Queries:        {len(synthetic_nequal_queries)}\n")
            for query in synthetic_nequal_queries:
                f.write(f"  Query: {query}\n")
            f.write(f"--------------------------------------\n")
            f.write(f"Synthetic Error Queries:            {len(synthetic_error_queries)}\n")
            for query in synthetic_error_queries:
                f.write(f"  Query: {query}\n")