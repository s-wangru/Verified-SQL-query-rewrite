import duckdb
import argparse

parser = argparse.ArgumentParser(description="Test generated data on query pairs")
parser.add_argument("--workload_path", type=str)
parser.add_argument("--schema_path", type=str, default=None)
parser.add_argument("--load_path", type=str, default=None)
args = parser.parse_args()

conn = duckdb.connect(database=':memory:')
with open (args.schema_path, 'r') as f:
    sql = f.read()
    conn.execute(sql)
    conn.commit()

with open (args.load_path, 'r') as f:
    sql = f.read()
    conn.execute(sql)
    conn.commit()

equals = 0
nequals = 0
errors = 0
with open(args.workload_path, 'r') as f:
    queries = f.read()
    queries = queries.split('User Query: ')
    for q in queries:
        qs = q.split('Optimized Query: ')
        if len(qs) < 2:
            continue
        orig = qs[0].strip()
        optimized = qs[1].strip()
        df_orig = conn.execute(orig).fetchdf()
        try:
            df_optim = conn.execute(optimized).fetchdf()
        except Exception as e:
            # print(f"Error executing optimized query: {e}")
            errors += 1
            print("The query not supported in duckdb ")

        if df_orig.equals(df_optim):
            equals += 1
            print("The query results are equal.")
        else:
            nequals += 1
            print("The query results are not equal.")

print(f"Equals: {equals}")
print(f"Not Equals: {nequals}")
print(f"Errors: {errors}")