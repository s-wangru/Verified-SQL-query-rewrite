import os
import openai
import argparse

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

def generate_query_pairs(workload_path, workload_stats):
    query_pairs = []

    with os.scandir(workload_path) as entries:
        for entry in entries:
            if entry.name.endswith('.sql') and entry.is_file() and entry.name.startswith('query'):
                with open(entry.path, 'r') as f:
                    user_query = f.read()
                    optimized_query = get_optimized_query(user_query, workload_stats)
                    query_pairs.append((user_query, optimized_query))

    return query_pairs

def write_output_file(query_pairs, output_file):
    with open(output_file, 'w') as f:
        for user_query, optimized_query in query_pairs:
            print(f"User Query: {user_query}")
            print(f"Optimized Query: {optimized_query}")
            f.write(f"User Query: {user_query}\n")
            f.write(f"Optimized Query: {optimized_query}\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate optimized SQL queries.")
    parser.add_argument("--workload_path", type=str)
    parser.add_argument("--schema_path", type=str, default=None)
    parser.add_argument("--stats_path", type=str, default=None)
    args = parser.parse_args()

    with open(args.schema_path, 'r') as f:
        schema = f.read()
    with open (args.stats_path, 'r') as f:
        stats = f.read()
    workload_stats = schema + '\n' + stats

    query_pairs = generate_query_pairs(args.workload_path, workload_stats)

    output_file = os.path.join(args.workload_path, 'optimized_queries.txt')
    write_output_file(query_pairs, output_file)