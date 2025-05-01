import re
import random
from faker import Faker
import argparse
import os


fake = Faker()
DELIMITER = "|"
INT32_MAX = 2**31 - 1
INT32_MIN = -2**31


def parse_schema(schema_sql):
    inside_parens = re.search(r'\((.*)\)', schema_sql, re.DOTALL).group(1)
    # requires every col name in schema to be on a new line
    lines = [line.strip().rstrip(',') for line in inside_parens.strip().splitlines()]
    columns = []

    for line in lines:
        match = re.match(r'(\w+)\s+(\S+)[ ,]*', line)
        if match:
            col_name, col_type = match.groups()
            upper_col_type = col_type.upper()
            if upper_col_type != "KEY" and upper_col_type != "TABLE":
                columns.append((col_name, upper_col_type))

    return columns


def generate_value(col_type):
    match = re.match(r'(\w+)(?:\((\d+)(?:,(\d+))?\))?', col_type)
    if not match:
        raise ValueError(f"Invalid column type: {col_type}")

    size = int(match.group(2)) if match.group(2) else None
    precision = int(match.group(3)) if match.group(3) else None

    if "INT" in col_type:
        return str(random.randint(INT32_MIN, INT32_MAX))
    elif "CHAR" in col_type or "TEXT" in col_type or "STRING" in col_type:
        return ''.join(fake.random_letter() for _ in range(size)) if size else fake.word()
    elif "DATE" in col_type:
        return fake.date_this_decade().isoformat()
    elif "TIME" in col_type:
        return fake.time()
    elif "TIMESTAMP" in col_type:
        return fake.date_time_this_decade().isoformat(sep=" ")
    elif "DOUBLE" in col_type or "FLOAT" in col_type or "REAL" in col_type:
        return f"{random.uniform(-1000.0, 1000.0):.2f}"
    elif "BOOLEAN" in col_type:
        return str(random.choice([True, False]))
    elif "DECIMAL" in col_type or "NUMERIC" in col_type:
        return f"{random.uniform(-1.0 * (size - 1) - 1, 1.0 * (size - 1) - 1):.{precision}f}" if size and precision else f"{random.uniform(-1000.0, 1000.0):.2f}"


def generate_dat_file(schema_sql, num_rows, filename):
    columns = parse_schema(schema_sql)
    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(num_rows):
            row = [generate_value(col_type) for _, col_type in columns]
            f.write(DELIMITER.join(row) + DELIMITER + "\n")


def generate_data(schema_path, output_path, num_rows):
    with open(schema_path, 'r') as f:
        schema = f.read()

        for s in schema.split(';'):
            stripped_s = s.strip()
            if stripped_s:
                ind_schema = stripped_s + ";\n"
                pattern = r"CREATE TABLE\s+(\w+)"
                match = re.search(pattern, ind_schema, re.IGNORECASE)

                if match:
                    table_name = match.group(1)
                    os.makedirs(output_path, exist_ok=True)
                    generate_dat_file(ind_schema, num_rows, output_path + '/' + table_name + ".dat")
                    print(f"Generated {num_rows} rows for table {table_name} in {output_path}/{table_name}.dat")
                else:
                    raise ValueError("Table name not found in the schema.")
                
def generate_copy_statements(schema_path, data_csv_path, load_output_path):
    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    with open(load_output_path, 'w') as f:
        table_pattern = re.compile(r'CREATE TABLE\s+(\w+)', re.IGNORECASE)
        tables = table_pattern.findall(schema_sql)

        for table in tables:
            statement = f"COPY {table} FROM '{data_csv_path}/{table}.dat' (DELIMITER '|', HEADER, IGNORE_ERRORS);"
            f.write(statement + '\n')

        print(f"SQL file written to: {load_output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic data to test query equivalence")
    parser.add_argument("--schema_path", type=str, default=None)
    parser.add_argument("--data_output_path", type=str, default=None)
    parser.add_argument("--num_rows", type=int, default=100)
    parser.add_argument("--load_output_path", type=str, default=None)
    args = parser.parse_args()

    generate_data(args.schema_path, args.data_output_path, args.num_rows)
    if args.load_output_path:
        generate_copy_statements(args.schema_path, args.data_output_path, args.load_output_path)