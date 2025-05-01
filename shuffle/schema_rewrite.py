#!/usr/bin/env python3

"""
schema_shuffle.py

Shuffle SQL schema identifiers and definitions, load nouns from an external file,
rename .dat files, and rewrite a separate load SQL file to use the new table names.

Usage:
    python schema_shuffle.py \
        --schema <input_schema.sql> [--output-schema <shuffled_schema.sql>] \
        --load-sql <input_load.sql> [--output-load-sql <rewritten_load.sql>] \
        --nouns-file <nouns.txt> \
        [--dat-dir <input_dat_folder> --output-dat-dir <output_dat_folder>]

Options:
  --schema             Path to original schema SQL file (required).
  --output-schema      Path for shuffled schema SQL (default: shuffled_schema.sql).
  --load-sql           Path to original load SQL file whose table names should be rewritten (required).
  --output-load-sql    Path for rewritten load SQL (default: rewritten_load.sql).
  --nouns-file, -n     Text file containing nouns (one per line) for identifier replacement (required).
  --dat-dir            Directory of .dat files named after original tables.
  --output-dat-dir     Directory to write renamed .dat files.
"""
import re
import random
import os
import json
import argparse
import shutil

# Pattern to detect SQL data types in column definitions
DATATYPE_PATTERN = r'(?:varchar|char|integer|decimal|date|time)'


def load_nouns(path):
    """Load noun list from a text file, one per line."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Nouns file not found: {path}")
    nouns = [line.strip() for line in open(path, 'r', encoding='utf-8') if line.strip()]
    if not nouns:
        raise ValueError(f"No nouns found in {path}")
    return nouns


def load_file(path):
    """Read entire file content."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def save_file(content, path):
    """Write content to file."""
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def extract_table_names(sql):
    """Find all table names in CREATE TABLE statements."""
    return re.findall(r'CREATE\s+TABLE\s+(\w+)', sql, re.IGNORECASE)


def extract_column_names(sql):
    """Extract column names by scanning CREATE TABLE blocks."""
    cols = set()
    blocks = re.findall(
        r'CREATE\s+TABLE\s+\w+\s*\((.*?)\)\s*;',
        sql, flags=re.IGNORECASE | re.DOTALL
    )
    for block in blocks:
        for line in block.splitlines():
            line = line.strip().rstrip(',')
            if not line or line.lower().startswith(('primary key', 'constraint', 'unique', 'foreign key')):
                continue
            m = re.match(r'([a-zA-Z_]\w*)\s+' + DATATYPE_PATTERN, line, re.IGNORECASE)
            if m:
                cols.add(m.group(1))
    return cols


def build_mapping(table_names, column_names, nouns):
    """Shuffle nouns and assign to tables and columns."""
    pool = nouns.copy()
    random.shuffle(pool)
    mapping = {}
    # Map tables
    for dat in table_names:
        if not pool:
            raise RuntimeError("Ran out of nouns mapping tables.")
        mapping[dat] = pool.pop()
    # Map columns
    for col in column_names:
        if col in mapping:
            continue
        if not pool:
            mapping[col] = f"{col}_col"
        else:
            mapping[col] = pool.pop()
    return mapping


def replace_identifiers(sql, mapping):
    """Replace identifiers in SQL (both backticks and unquoted)."""
    # Backtick-quoted
    def bt(m): return f"`{mapping.get(m.group(1), m.group(1))}`"
    sql = re.sub(r'`(\w+)`', bt, sql)
    # Unquoted word boundaries
    if mapping:
        pat = r"\b(" + "|".join(re.escape(k) for k in mapping) + r")\b"
        sql = re.sub(pat, lambda m: mapping.get(m.group(1), m.group(1)), sql)
    return sql


def shuffle_definitions(sql):
    """Shuffle the order of CREATE TABLE definitions."""
    blocks = re.findall(r'(CREATE\s+TABLE.*?;)', sql, flags=re.IGNORECASE | re.DOTALL)
    random.shuffle(blocks)
    return '\n\n'.join(blocks)


def rename_dat_files(mapping, dat_dir, output_dat_dir):
    """Copy and rename .dat files based on table mapping."""
    if not os.path.isdir(dat_dir):
        raise NotADirectoryError(f".dat directory not found: {dat_dir}")
    os.makedirs(output_dat_dir, exist_ok=True)
    for fname in os.listdir(dat_dir):
        if not fname.lower().endswith('.dat'):
            continue
        orig = os.path.splitext(fname)[0]
        new = mapping.get(orig)
        if new:
            shutil.copy2(
                os.path.join(dat_dir, fname),
                os.path.join(output_dat_dir, new + '.dat')
            )
            print(f"Copied: {fname} -> {new}.dat")
        else:
            print(f"Skipping {fname}: no mapping")


def main():
    parser = argparse.ArgumentParser(description="Shuffle schema, rewrite load SQL, and rename .dat files.")
    parser.add_argument('--schema', required=True, help="Input schema SQL file")
    parser.add_argument('--output-schema', default='shuffled_schema.sql', help="Shuffled schema output file")
    parser.add_argument('--load-sql', required=True, help="Input load SQL to rewrite table names")
    parser.add_argument('--output-load-sql', default='rewritten_load.sql', help="Rewritten load SQL output file")
    parser.add_argument('-n', '--nouns-file', default="nouns.txt", help="File with nouns (one per line)")
    parser.add_argument('--dat-dir', help="Directory of .dat files to rename")
    parser.add_argument('--output-dat-dir', help="Directory for renamed .dat files")
    args = parser.parse_args()

    # Paths
    schema_in = args.schema
    schema_out = args.output_schema
    load_in = args.load_sql
    load_out = args.output_load_sql
    mapping_path = os.path.splitext(schema_out)[0] + '_mapping.json'

    # Load data
    nouns = load_nouns(args.nouns_file)
    schema_sql = load_file(schema_in)
    dats = extract_table_names(schema_sql)
    cols = extract_column_names(schema_sql)
    mapping = build_mapping(dats, cols, nouns)

    new_schema = shuffle_definitions(replace_identifiers(schema_sql, mapping))
    save_file(new_schema, schema_out)
    print(f"Shuffled schema written to {schema_out}")

    with open(mapping_path, 'w', encoding='utf-8') as mf:
        json.dump(mapping, mf, indent=2)
    print(f"Mapping JSON written to {mapping_path}")

    load_sql = load_file(load_in)
    new_load = replace_identifiers(load_sql, mapping)
    save_file(new_load, load_out)
    print(f"Rewritten load SQL written to {load_out}")

    if args.dat_dir and args.output_dat_dir:
        rename_dat_files(mapping, args.dat_dir, args.output_dat_dir)

if __name__ == '__main__':
    main()
