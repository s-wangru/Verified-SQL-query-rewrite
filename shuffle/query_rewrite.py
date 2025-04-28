#!/usr/bin/env python3

"""
rewrite_queries.py

This script rewrites all SQL query files in a workload to match a renamed/shuffled schema.
It expects a mapping JSON produced by your schema_shuffle tool, where keys are original identifiers
and values are the new nouns. Optionally, it can apply column renaming if enabled.

Usage:
    python rewrite_queries.py mapping.json /path/to/original/queries /path/to/output/queries [--rewrite-columns]

If the input path is a directory, it recursively processes all `.sql` files, preserving directory structure.
"""
import argparse
import json
import os
import re
import sys


def load_mapping(path):
    """Load mapping JSON from disk."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def replace_identifiers(sql, mapping):
    def backtick_repl(m):
        orig = m.group(1)
        return f"`{mapping.get(orig, orig)}`"
    sql = re.sub(r'`(\w+)`', backtick_repl, sql)

    if mapping:
        pattern = r"\b(" + "|".join(re.escape(k) for k in mapping.keys()) + r")\b"
        sql = re.sub(pattern, lambda m: mapping.get(m.group(1), m.group(1)), sql)
    return sql


def process_file(in_path, out_path, mapping):
    with open(in_path, 'r', encoding='utf-8') as f:
        content = f.read()
    rewritten = replace_identifiers(content, mapping)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rewritten)
    print(f"Rewritten: {in_path} -> {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Rewrite SQL workload queries according to a mapping JSON."
    )
    parser.add_argument('mapping', help="Path to mapping JSON file (original->new identifiers)")
    parser.add_argument('input', help="Input .sql file or directory of SQL queries")
    parser.add_argument('output', help="Output file or directory for rewritten queries")
    parser.add_argument('--rewrite-columns', '-c', action='store_true',
                        help="Also apply column identifier replacements (requires mapping JSON with column entries)")
    args = parser.parse_args()

    raw_map = load_mapping(args.mapping)
    if isinstance(raw_map, dict) and 'tables' in raw_map:
        table_map = raw_map.get('tables', {})
        column_map = raw_map.get('columns', {})
    else:
        table_map = raw_map
        column_map = {}

    if args.rewrite_columns:
        mapping = {**table_map, **column_map}
    else:
        mapping = table_map

    inp = args.input
    outp = args.output

    if os.path.isdir(inp):
        for root, _, files in os.walk(inp):
            for fname in files:
                if not fname.lower().endswith('.sql') or fname.lower().endswith('tables.sql'):
                    continue
                rel = os.path.relpath(os.path.join(root, fname), inp)
                in_path = os.path.join(root, fname)
                out_path = os.path.join(outp, rel)
                process_file(in_path, out_path, mapping)
    else:
        process_file(inp, outp, mapping)


if __name__ == '__main__':
    main()
