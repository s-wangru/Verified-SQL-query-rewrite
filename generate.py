import re
import random
from faker import Faker
import argparse


parser = argparse.ArgumentParser(description="Generate optimized SQL queries.")
parser.add_argument("--workload_path", type=str)
parser.add_argument("--schema_path", type=str, default=None)
parser.add_argument("--output_path", type=str, default=None)
parser.add_argument("--num_rows", type=int, default=100)
args = parser.parse_args()


fake = Faker()
DELIMITER = "|"
INT32_MAX = 2**31 - 1
INT32_MIN = -2**31


def parse_schema(schema_sql):
    inside_parens = re.search(r'\((.*)\)', schema_sql, re.DOTALL).group(1)
    lines = [line.strip().rstrip(',') for line in inside_parens.strip().splitlines()]
    columns = []

    for line in lines:
        match = re.match(r'(\w+)\s+(\w+)', line)
        if match:
            col_name, col_type = match.groups()
            upper_col_type = col_type.upper()
            if upper_col_type != "KEY" and upper_col_type != "TABLE":
                columns.append((col_name, upper_col_type))

    return columns


def generate_value(col_type):
    if "INT" in col_type:
        return str(random.randint(INT32_MIN, INT32_MAX))
    elif "CHAR" in col_type or "TEXT" in col_type or "STRING" in col_type:
        return fake.word()
    elif "DATE" in col_type:
        return fake.date_this_decade().isoformat()
    elif "TIME" in col_type:
        return fake.time()
    elif "TIMESTAMP" in col_type:
        return fake.date_time_this_decade().isoformat(sep=" ")
    elif "DOUBLE" in col_type or "FLOAT" in col_type or "REAL" in col_type:
        return f"{random.uniform(1.0, 1000.0):.2f}"
    elif "BOOLEAN" in col_type:
        return str(random.choice([True, False]))
    elif "DECIMAL" in col_type or "NUMERIC" in col_type:
        return f"{random.uniform(1.0, 1000.0):.2f}"


def generate_dat_file(schema_sql, num_rows, filename):
    columns = parse_schema(schema_sql)
    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(num_rows):
            row = [generate_value(col_type) for _, col_type in columns]
            f.write(DELIMITER.join(row) + DELIMITER + "\n")


with open(args.schema_path, 'r') as f:
    schema = f.read()
    for s in schema.split(';'):
        if s.strip():
            ind_schema = s + ";\n"
            pattern = r"CREATE TABLE\s+(\w+)"
            match = re.search(pattern, ind_schema, re.IGNORECASE)

            if match:
                table_name = match.group(1)

                generate_dat_file(ind_schema, args.num_rows, args.output_path + '/' + table_name + ".dat")
                print(f"Generated {args.num_rows} rows for table {table_name} in {args.output_path}/{table_name}.dat")
            else:
                print("Table name not found in the schema.")
        else:
            print(s)