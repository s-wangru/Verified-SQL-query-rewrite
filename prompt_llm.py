#!/usr/bin/env python3

import os
import openai
import argparse

# Ensure API key is set
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

PROMPT = (
    "Your job is to rewrite SQL queries to optimize performance in DuckDB. "
    "Make sure it has the same output and doesn't modify the predicates even if it seems wrong. "
    "Only output the optimized query in one line, don't include any other additional words or newline characters. "
    "You are given the following workload stats (table cardinalities) and schema to help you with rewriting the queries:\n"
)

def get_optimized_query(user_query, workload_stats):
    messages = [
        {"role": "system", "content": PROMPT + workload_stats},
        {"role": "user", "content": user_query}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def load_file(path):
    """Read entire file content."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_query_pairs(workload_path, workload_stats):
    query_pairs = []
    for entry in os.scandir(workload_path):
        if entry.is_file() and entry.name.endswith('.sql') and entry.name.startswith('query'):
            with open(entry.path, 'r', encoding='utf-8') as f:
                user_query = f.read().strip()
            optimized = get_optimized_query(user_query, workload_stats)
            query_pairs.append((user_query, optimized))
    return query_pairs


def write_output_file(query_pairs, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for user_query, optimized_query in query_pairs:
            f.write(f"User Query: {user_query}\n")
            f.write(f"Optimized Query: {optimized_query}\n\n")
    print(f"Optimized queries written to {output_file}")

import re
DATATYPE_PATTERN = r'(?:varchar|char|integer|decimal|date|time)'

def extract_schema_columns(sql):
    """
    Parse the schema SQL and return a dict mapping each table to its ordered list of column names.
    """
    tables = {}
    # Find each CREATE TABLE block with its columns
    for match in re.finditer(
        r'CREATE\s+TABLE\s+(\w+)\s*\((.*?)\)\s*;',
        sql,
        flags=re.IGNORECASE | re.DOTALL
    ):
        table = match.group(1)
        cols_block = match.group(2)
        cols = []
        for line in cols_block.splitlines():
            line = line.strip().rstrip(',')
            if not line or line.lower().startswith(('primary key', 'constraint', 'unique', 'foreign key')):
                continue
            m = re.match(r'([a-zA-Z_]\w*)\s+' + DATATYPE_PATTERN, line, re.IGNORECASE)
            if m:
                cols.append(m.group(1))
        tables[table] = cols
    return tables


def compute_stats(dat_dir, schema_sql):
    schema_cols = extract_schema_columns(schema_sql)
    stats_lines = []

    for entry in os.scandir(dat_dir):
        if not entry.is_file() or not entry.name.endswith('.dat'):
            continue
        table = os.path.splitext(entry.name)[0]
        cols = schema_cols.get(table)
        if not cols:
            print(f"Warning: no schema definition for {table}, skipping stats.")
            continue
        distinct_sets = {col: set() for col in cols}
        row_count = 0
        path = os.path.join(dat_dir, entry.name)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                row_count += 1
                fields = line.rstrip('\n').rstrip('|').split('|')
                for idx, col in enumerate(cols):
                    if idx < len(fields):
                        val = fields[idx]
                        if val:
                            distinct_sets[col].add(val)
        stats_lines.append(f"{table}: {row_count} rows")
        for col in cols:
            distinct_count = len(distinct_sets[col])
            selectivity = distinct_count / row_count if row_count else 0
            stats_lines.append(
                f"{table}.{col}: distinct={distinct_count}, selectivity={selectivity:.4f}"
            )
    return '\n'.join(stats_lines)



def main():
    parser = argparse.ArgumentParser(
        description="Generate optimized SQL queries using schema and .dat stats."
    )
    parser.add_argument("--workload_path", required=True, help="Directory containing SQL workload files")
    parser.add_argument("--schema_path", required=True, help="Path to the schema SQL file")
    parser.add_argument("--dat_dir", required=True, help="Directory containing .dat files for stats")
    args = parser.parse_args()

    with open(args.schema_path, 'r', encoding='utf-8') as f:
        schema = f.read().strip()

    stats_text = compute_stats(args.dat_dir)

    workload_stats = schema + '\n' + stats_text

    pairs = generate_query_pairs(args.workload_path, workload_stats)

    output_file = os.path.join(args.workload_path, 'optimized_queries.txt')
    write_output_file(pairs, output_file)

if __name__ == "__main__":
    main()
