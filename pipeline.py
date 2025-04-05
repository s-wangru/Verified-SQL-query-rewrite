import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


prompt = "Your job is to rewrite SQL queries to optimize performance in duckdb. Make sure it has the same output and don't modify the predicates even if it seems wrong. \
            Only output the optimized query in one line, don't include any other additional words and newline characters\
            You are given the following workload stats and schema to help you with rewriting the queries: "
workload_stats = "given the cardinalities of the table: Loaded 75000 rows from customer (Parquet).\
                Loaded 25 rows from nation (Parquet).\
                Loaded 750000 rows from orders (Parquet).\
                Loaded 100000 rows from part (Parquet).\
                Loaded 400000 rows from partsupp (Parquet).\
                Loaded 5 rows from region (Parquet).\
                Loaded 5000 rows from supplier (Parquet).\
                Loaded 2999671 rows from lineitem (Parquet).\
                and the schema: \
                CREATE TABLE customer(c_custkey BIGINT NOT NULL, c_name VARCHAR NOT NULL, c_address VARCHAR NOT NULL, c_nationkey INTEGER NOT NULL, c_phone VARCHAR NOT NULL, c_acctbal DECIMAL(15,2) NOT NULL, c_mktsegment VARCHAR NOT NULL, c_comment VARCHAR NOT NULL);\
                CREATE TABLE lineitem(l_orderkey BIGINT NOT NULL, l_partkey BIGINT NOT NULL, l_suppkey BIGINT NOT NULL, l_linenumber BIGINT NOT NULL, l_quantity DECIMAL(15,2) NOT NULL, l_extendedprice DECIMAL(15,2) NOT NULL, l_discount DECIMAL(15,2) NOT NULL, l_tax DECIMAL(15,2) NOT NULL, l_returnflag VARCHAR NOT NULL, l_linestatus VARCHAR NOT NULL, l_shipdate DATE NOT NULL, l_commitdate DATE NOT NULL, l_receiptdate DATE NOT NULL, l_shipinstruct VARCHAR NOT NULL, l_shipmode VARCHAR NOT NULL, l_comment VARCHAR NOT NULL);\
                CREATE TABLE nation(n_nationkey INTEGER NOT NULL, n_name VARCHAR NOT NULL, n_regionkey INTEGER NOT NULL, n_comment VARCHAR NOT NULL);\
                CREATE TABLE orders(o_orderkey BIGINT NOT NULL, o_custkey BIGINT NOT NULL, o_orderstatus VARCHAR NOT NULL, o_totalprice DECIMAL(15,2) NOT NULL, o_orderdate DATE NOT NULL, o_orderpriority VARCHAR NOT NULL, o_clerk VARCHAR NOT NULL, o_shippriority INTEGER NOT NULL, o_comment VARCHAR NOT NULL);\
                CREATE TABLE part(p_partkey BIGINT NOT NULL, p_name VARCHAR NOT NULL, p_mfgr VARCHAR NOT NULL, p_brand VARCHAR NOT NULL, p_type VARCHAR NOT NULL, p_size INTEGER NOT NULL, p_container VARCHAR NOT NULL, p_retailprice DECIMAL(15,2) NOT NULL, p_comment VARCHAR NOT NULL);\
                CREATE TABLE partsupp(ps_partkey BIGINT NOT NULL, ps_suppkey BIGINT NOT NULL, ps_availqty BIGINT NOT NULL, ps_supplycost DECIMAL(15,2) NOT NULL, ps_comment VARCHAR NOT NULL);\
                CREATE TABLE region(r_regionkey INTEGER NOT NULL, r_name VARCHAR NOT NULL, r_comment VARCHAR NOT NULL);\
                CREATE TABLE supplier(s_suppkey BIGINT NOT NULL, s_name VARCHAR NOT NULL, s_address VARCHAR NOT NULL, s_nationkey INTEGER NOT NULL, s_phone VARCHAR NOT NULL, s_acctbal DECIMAL(15,2) NOT NULL, s_comment VARCHAR NOT NULL);\
                CREATE VIEW revenue0r15721 (supplier_no, total_revenue) AS SELECT l_suppkey, sum(l_extendedprice * (1 - l_discount)) FROM lineitem WHERE l_shipdate >= DATE '1995-01-01' AND l_shipdate < DATE '1995-01-01' + INTERVAL '3' MONTH GROUP BY l_suppkey; "
                                    

def get_optimized_query(user_query):
    tmp_messages = messages.copy()
    tmp_messages.append({"role": "user", "content": user_query})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=tmp_messages
    )

    reply = response['choices'][0]['message']['content']
    return reply

query_pairs = []

import argparse

parser = argparse.ArgumentParser(description="Generate optimized SQL queries.")
parser.add_argument("--workload_path", type=str)
parser.add_argument("--schema_path", type=str, default=None)
parser.add_argument("--stats_path", type=str, default=None)
args = parser.parse_args()

workload_path = args.workload_path
with open(args.schema_path, 'r') as f:
    schema = f.read()
with open (args.stats_path, 'r') as f:
    stats = f.read()
workload_stats = schema + '\n' + stats

messages = [
    {"role": "system", "content": prompt + '\n' + workload_stats}
]

# workload_path is a directory
with os.scandir(workload_path) as entries:
    for entry in entries:
        if entry.name.endswith('.sql') and entry.is_file() and entry.name.startswith('query'):
            with open(entry.path, 'r') as f:
                user_query = f.read()
                optimized_query = get_optimized_query(user_query)
                query_pairs.append((user_query, optimized_query))
                print(f"User Query: {user_query}")
                print(f"Optimized Query: {optimized_query}")

# Save the query pairs to a file
output_file = os.path.join(workload_path, 'optimized_queries.txt')
with open(output_file, 'w') as f:
    for user_query, optimized_query in query_pairs:
        f.write(f"User Query: {user_query}\n")
        f.write(f"Optimized Query: {optimized_query}\n\n")