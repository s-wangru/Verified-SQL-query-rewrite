#!/usr/bin/env python3
import re
import random
import sys
import os
import json


DATATYPE_PATTERN = r'(?:varchar|char|integer|decimal|date|time)'


def load_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def save_schema(content, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def extract_table_names(sql):
    return re.findall(r'CREATE\s+TABLE\s+(\w+)', sql, re.IGNORECASE)


def extract_column_names(sql):
    cols = set()

    for col_block in re.findall(
        r'CREATE\s+TABLE\s+\w+\s*\((.*?)\)\s*;',
        sql,
        flags=re.IGNORECASE | re.DOTALL
    ):
        for line in col_block.splitlines():
            line = line.strip()
            if not line or line.lower().startswith(('primary key', 'constraint', 'unique', 'foreign key')):
                continue
            m = re.match(r'([a-zA-Z_]\w*)\s+' + DATATYPE_PATTERN, line, re.IGNORECASE)
            if m:
                cols.add(m.group(1))
    return cols


def build_mapping(table_names, column_names, nouns):
    nouns = nouns.copy()
    random.shuffle(nouns)
    mapping = {}
    col_map = {}

    for tbl in table_names:
        if not nouns:
            raise RuntimeError("Ran out of nouns when mapping tables.")
        mapping[tbl] = nouns.pop()

    for col in column_names:
        cols = col.split('_')
        abb = cols[0]
        name = col[len(abb):]
        print(name)
        if col in mapping:
            continue
        if name in col_map:
            newcol = abb + '_' + col_map[name]
            mapping[col] = newcol
            continue
        if not nouns:
            mapping[col] = f"{col}_col"
        else:
            new_name = nouns.pop()
            col_map[name] = new_name
            mapping[col] = abb + '_' + new_name
    return mapping


def replace_identifiers(sql, mapping):
    def backtick_repl(m):
        name = m.group(1)
        return f"`{mapping.get(name, name)}`"
    sql = re.sub(r'`(\w+)`', backtick_repl, sql)

    if mapping:
        pattern = r"\b(" + "|".join(re.escape(k) for k in mapping.keys()) + r")\b"
        sql = re.sub(pattern, lambda m: mapping.get(m.group(1), m.group(1)), sql)
    return sql


def shuffle_definitions(sql):
    blocks = re.findall(r'(CREATE\s+TABLE.*?;)', sql, flags=re.IGNORECASE | re.DOTALL)
    random.shuffle(blocks)
    return '\n\n'.join(blocks)


def main():
    if len(sys.argv) < 2:
        print("Usage: schema_shuffle.py <input_schema.sql> [output_schema.sql]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'shuffled_schema.sql'
    with open('nouns.txt', 'r', encoding='utf-8') as f:
        nouns = f.read().splitlines()

    base, _ = os.path.splitext(output_path)
    mapping_path = f"{base}_mapping.json"

    sql = load_schema(input_path)
    tables = extract_table_names(sql)
    cols = extract_column_names(sql)
    mapping = build_mapping(tables, cols, nouns)

    sql_replaced = replace_identifiers(sql, mapping)
    shuffled_sql = shuffle_definitions(sql_replaced)

    save_schema(shuffled_sql, output_path)
    print(f"Shuffled schema written to {output_path}")

    with open(mapping_path, 'w', encoding='utf-8') as mf:
        json.dump(mapping, mf, indent=2)
    print(f"Mapping JSON written to {mapping_path}")


if __name__ == '__main__':
    main()
