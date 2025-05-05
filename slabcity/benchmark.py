import duckdb
import json
import csv
import tempfile
import shutil
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import openai
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

PROMPT = "Your job is to rewrite SQL queries to optimize performance in DuckDB. Make sure it has the same output and doesn't modify the predicates even if it seems wrong. \
            Only output the optimized query in one line, don't include any other additional words and newline characters\
            You are given the following workload stats (table cardinalities) and schema to help you with rewriting the queries: "

def get_optimized_query(user_query, workload_stats):
    tmp_messages = [
        {"role": "system", "content": PROMPT + '\n' + workload_stats}
    ]
    tmp_messages.append({"role": "user", "content": user_query})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=tmp_messages
    )

    reply = response['choices'][0]['message']['content']
    return reply

def preprocess_csv_skip_line(original_path):
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".csv")

    with open(original_path, 'r') as src, temp_file as dst:
        next(src)
        shutil.copyfileobj(src, dst)

    return temp_file.name

def create_tables(conn, tables):
    # create all tables
    schemastr = ""
    for table in tables:
        table_name = table["TableName"]

        all_columns = {}

        for col in table["PKeys"]:
            col_name = col["Name"]
            col_type = col["Type"]
            if col_name not in all_columns:
                if col_type.startswith("enum") or col_type.startswith("ENUM"):
                    _, *values = col_type.split(",")
                    enum_check = f"TEXT CHECK ({col_name} IN ({', '.join(repr(v) for v in values)}))"
                    all_columns[col_name] = enum_check
                else:
                    all_columns[col_name] = col_type

        for fk in table.get("FKeys", []):
            if fk["FName"] not in all_columns:
                all_columns[fk["FName"]] = "int"

        for col in table.get("Others", []):
            col_name = col["Name"]
            col_type = col["Type"]
            if col_name not in all_columns:
                if col_type.startswith("enum") or col_type.startswith("ENUM"):
                    _, *values = col_type.split(",")
                    enum_check = f"TEXT CHECK ({col_name} IN ({', '.join(repr(v) for v in values)}))"
                    all_columns[col_name] = enum_check
                else:
                    all_columns[col_name] = col_type

        column_defs = [f"{name} {dtype}" for name, dtype in all_columns.items()]

        if table["PKeys"]:
            pk_cols = ", ".join(col["Name"] for col in table["PKeys"])
            column_defs.append(f"PRIMARY KEY ({pk_cols})")

        # skip over foreign keys for now

        create_stmt = f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(column_defs) + "\n);"
        schemastr += create_stmt + "\n"

        try:
            conn.execute(create_stmt)
        except Exception as e:
            print(f"Error creating table {table_name} with {e}")
            print(f"Tried to run:\n{create_stmt}\n")
            return None
        
    return schemastr

def load_tables(conn, datapath, tables):
    # load data into tables
    loadstr = ""
    for i, table in enumerate(tables):
        table_name = table["TableName"]
        csv_file = f"{datapath}{table_name}.csv"
        clean_csv = preprocess_csv_skip_line(csv_file)
        # print(f"Loading data from {clean_csv} into {table_name}")
        
        try:
            conn.execute(f"COPY {table_name} FROM '{clean_csv}' (DELIMITER ',', HEADER TRUE);")
            loadstr += f"COPY {table_name} FROM '{clean_csv}' (DELIMITER ',', HEADER TRUE);\n"
        except Exception as e:
            print(f"Error loading table {table_name}: {e}")
            return None
    
    return loadstr

def warmup_database(conn, tables):
    # warm up database
    cardinality = ""
    for table in tables:
        table_name = table["TableName"]
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()
        numrows = result[0] 
        cardinality += f'{table_name}: {numrows}\n'

    return cardinality

def find_queries(querypath):
    queries = {}
    with open(querypath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 2:
                continue
            id = row[0].strip()
            query = row[1].strip()
            queries[id] = query + ";"

    return queries

def execute_queries(conn, queries):
    timemap = {}
    errors = set()
    for _ in range(3):
        for id, query in queries.items():
            if id in errors:
                continue

            print(f"Executing query {id}")
            start = time.time()
            try:
                conn.execute(query)
            except Exception as e:
                timemap[id] = 0
                errors.add(id)
                continue
            end = time.time()
            elapsed_time = end - start
            if id in timemap:
                timemap[id] += elapsed_time
            else:
                timemap[id] = elapsed_time

    if errors:
        print("Errors executing queries:")
        for id in errors:
            print(f"    {id}")

    return timemap

def check_query_equivalence(conn, query1, query2):
    try:
        df1 = conn.execute(query1).fetchdf()
        df2 = conn.execute(query2).fetchdf()

        df1_sorted = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True)
        df2_sorted = df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

        if df1_sorted.equals(df2_sorted):
            return True
        else:
            # diff = pd.concat([df1_sorted, df2_sorted]).drop_duplicates(keep=False)
            # print(diff)
            return False
    except Exception as e:
        print(f"Error executing queries: {e}")
        return False

def get_timemap_list(timemap, notequiv):
    alltimes = []
    for id, elapsed_time in sorted(timemap.items()):
        # print(f"ID: {id}, Elapsed time: {(elapsed_time / 3):.4f} seconds")
        if id in notequiv:
            alltimes.append(0)
        else:
            alltimes.append(elapsed_time / 3)
    return alltimes

def plot_time_diff(problem, ids, duckdbopt_alltimes, noduckdbopt_alltimes, llmopt_alltimes, llmduckdbopt_alltimes):
    x = np.arange(len(ids))  # the label locations
    width = 0.15  # the width of the bars

    plt.figure(figsize=(14, 6))

    plt.bar(x - 1.5*width, duckdbopt_alltimes, width, label='DuckDB Opt On')
    plt.bar(x - 0.5*width, noduckdbopt_alltimes, width, label='DuckDB Opt Off')
    plt.bar(x + 0.5*width, llmopt_alltimes, width, label='LLM Opt')
    plt.bar(x + 1.5*width, llmduckdbopt_alltimes, width, label='LLM + DuckDB Opt')

    plt.xlabel('id')
    plt.ylabel('elapsed time (seconds)')
    plt.title(f'problem {problem}')
    plt.xticks(x, ids, rotation=90)
    plt.legend()
    plt.tight_layout()

    # show plot
    # plt.show()

    # save plot; make sure exist results/ directory
    os.makedirs('results/plots', exist_ok=True)
    plt.savefig(f"results/plots/{problem}.png", dpi=300)
    plt.close()

def populate_llm_optimized_queries(lc_type, problem, dataset_size):
    conn = duckdb.connect(":memory:")
    conn.execute("SET memory_limit='2GB';")

    datapath = f'data/databases/{lc_type}/{dataset_size}/{problem}/'
    schemapath = f'LeetCode/schemas/{problem}.json'
    querypath = f'LeetCode/queries/{problem}.csv'
    optimizedquerypath = f'optimized_queries/{problem}.csv'

    with open(schemapath) as f:
        schema_json = json.load(f)

    tables = schema_json["Tables"]

    schemastr = create_tables(conn, tables)
    if not schemastr:
        return
    
    if not load_tables(conn, datapath, tables):
        return
    
    queries = find_queries(querypath)
    
    cardinality = warmup_database(conn, tables)
    workload_stats = schemastr + cardinality
    
    os.makedirs('optimized_queries', exist_ok=True)
    with open(optimizedquerypath, 'w') as f:
        for id, query in queries.items():
            print(f"Optimizing query {id}")
            print(f"Original query: {query}")
            optimized_query = get_optimized_query(query, workload_stats).strip(';')
            print(f"Optimized query: {optimized_query}")
            f.write(f'{id},"{optimized_query}"\n')

def benchmark(lc_type, problem, dataset_size):
    datapath = f'data/databases/{lc_type}/{dataset_size}/{problem}/'
    schemapath = f'LeetCode/schemas/{problem}.json'
    querypath = f'LeetCode/queries/{problem}.csv'
    optimizedquerypath = f'optimized_queries/{problem}.csv'

    with open(schemapath) as f:
        schema_json = json.load(f)

    tables = schema_json["Tables"]

    # find queries
    queries = find_queries(querypath)
    optimized_queries = find_queries(optimizedquerypath)

    # ===================================

    conn = duckdb.connect(":memory:")
    conn.execute("SET memory_limit='2GB';")

    print("Num of queries:", len(queries))

    schemastr = create_tables(conn, tables)
    if not schemastr:
        return
    
    os.makedirs('llm_benchmark/schema', exist_ok=True)
    with open(f"llm_benchmark/schema/{problem}.sql", "w") as f:
        f.write(schemastr)
    
    loadstr = load_tables(conn, datapath, tables)
    if not loadstr:
        return
    
    os.makedirs('llm_benchmark/load', exist_ok=True)
    with open(f"llm_benchmark/load/{problem}.sql", "w") as f:
        f.write(loadstr)

    notequiv = set()
    os.makedirs('llm_benchmark/queries', exist_ok=True)
    with open(f"llm_benchmark/queries/{problem}.txt", "w") as f:
        for id, query in queries.items():
            optimizedquery = optimized_queries[id]
            f.write(f"User Query: {query}\n")
            f.write(f"Optimized Query: {optimizedquery}\n\n")
            if not check_query_equivalence(conn, query, optimizedquery):
                notequiv.add(id)
                # print(f"Queries {id} are not equivalent")
                # print(f"Original query: {query}")
                # print(f"Optimized query: {optimizedquery}")
                # print("=========================================")

    conn.close()

    # ===================================

    conn = duckdb.connect(":memory:")
    conn.execute("SET memory_limit='2GB';")

    if not create_tables(conn, tables):
        return
    
    if not load_tables(conn, datapath, tables):
        return

    warmup_database(conn, tables)
    duckopt_timemap = execute_queries(conn, queries)

    duckdbopt_alltimes = get_timemap_list(duckopt_timemap, notequiv)
    conn.close()

    # ==================================
    
    conn = duckdb.connect(":memory:")
    conn.execute("SET memory_limit='2GB';")

    create_tables(conn, tables)
    load_tables(conn, datapath, tables)

    conn.execute("PRAGMA disable_optimizer;")

    warmup_database(conn, tables)
    noduckopt_timemap = execute_queries(conn, queries)

    noduckdbopt_alltimes = get_timemap_list(noduckopt_timemap, notequiv)
    conn.close()

    # ==================================
    
    conn = duckdb.connect(":memory:")
    conn.execute("SET memory_limit='2GB';")

    create_tables(conn, tables)
    load_tables(conn, datapath, tables)

    conn.execute("PRAGMA disable_optimizer;")

    warmup_database(conn, tables)
    llmopt_timemap = execute_queries(conn, optimized_queries)

    llmopt_alltimes = get_timemap_list(llmopt_timemap, notequiv)
    conn.close()

    # ==================================
    
    conn = duckdb.connect(":memory:")
    conn.execute("SET memory_limit='2GB';")

    create_tables(conn, tables)
    load_tables(conn, datapath, tables)

    warmup_database(conn, tables)
    llmduckdbopt_timemap = execute_queries(conn, optimized_queries)

    llmduckdbopt_alltimes = get_timemap_list(llmduckdbopt_timemap, notequiv)
    conn.close()

    # ==================================

    sorted_ids = sorted(noduckopt_timemap.keys(), key=lambda x: int(x))
    plot_time_diff(problem, sorted_ids, duckdbopt_alltimes, noduckdbopt_alltimes, llmopt_alltimes, llmduckdbopt_alltimes)

    os.makedirs('results/times', exist_ok=True)
    with open(f"results/times/{problem}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "DuckDB Opt On", "DuckDB Opt Off", "LLM Opt", "LLM + DuckDB Opt"])
        for id in sorted_ids:
            writer.writerow([id, duckopt_timemap[id], noduckopt_timemap[id], llmopt_timemap[id], llmduckdbopt_timemap[id]])

    os.makedirs('results/notequivs', exist_ok=True)
    with open(f"results/notequivs/{problem}.txt", "w") as f:
        for id in notequiv:
            f.write(f"{id}: {queries[id]}\n")

if __name__ == "__main__":
    lc_type = "leetcode_uniform"
    dataset_size = "100K"

    directory = "LeetCode/queries/"
    file_names = [
        os.path.splitext(f)[0]
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    allproblems = sorted(file_names, key=lambda x: int(x))

    for problem in allproblems:
        # FIXED
        # for 1308, changed gender from enum type to varchar
        # for 1050, changed timestamp from primary key to others (since dup key issue)

        # UNFIXED
        # for 178, has timeouts
        # for 1532, not easily fixable since data generated has cols in wrong order

        if problem == "1532" or problem == "178":
            continue 

        print(f"Running problem {problem}")
        # populate_llm_optimized_queries(lc_type, problem, dataset_size)
        benchmark(lc_type, problem, dataset_size)
        print(f"Finished problem {problem}")
        print("=============================")