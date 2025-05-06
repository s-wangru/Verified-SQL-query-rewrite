#!/usr/bin/env python3
import os
import re
import tempfile
import duckdb
import openai
from flask import Flask, request, render_template_string, redirect, url_for, flash, send_file
from faker import Faker
import random

# ============ CONFIGURATION ============
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment")

PROMPT_TEMPLATE = (
    "Your job is to rewrite SQL queries to optimize performance in DuckDB. "
    "Make sure it has the same output and don't modify predicates even if they seem wrong. "
    "Only output the optimized query in one line, no extra words or newlines.\n"
)
DATATYPE_PATTERN = r"(?:varchar|char|integer|decimal|date|time)"
fake = Faker()
DELIMITER = "|"
INT32_MIN, INT32_MAX = -2**31, 2**31 - 1

# ============ HELPERS ============
def extract_schema_columns(sql_text):
    tables = {}
    for match in re.finditer(
        r"CREATE\s+TABLE\s+(\w+)\s*\((.*?)\)\s*;",
        sql_text, flags=re.IGNORECASE|re.DOTALL
    ):
        table = match.group(1)
        block = match.group(2)
        cols = []
        for line in block.splitlines():
            line = line.strip().rstrip(",")
            if not line or line.lower().startswith(("primary key","constraint","foreign","unique")):
                continue
            m = re.match(r"([a-zA-Z_]\w*)\s+"+DATATYPE_PATTERN, line, re.IGNORECASE)
            if m:
                cols.append(m.group(1))
        tables[table] = cols
    return tables

# Optimize via OpenAI
def optimize_query(schema, stats, user_sql):
    prompt = PROMPT_TEMPLATE + "Schema:\n" + schema + "\nStats:\n" + stats
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role":"system", "content": prompt},
            {"role":"user",   "content": user_sql}
        ]
    )
    return resp.choices[0].message.content.strip()




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


def generate_data(schema, output_path, num_rows):
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
            
                
def generate_copy_statements(schema_sql, data_csv_path, load_output_path):

    with open(load_output_path, 'w') as f:
        table_pattern = re.compile(r'CREATE TABLE\s+(\w+)', re.IGNORECASE)
        tables = table_pattern.findall(schema_sql)

        for table in tables:
            statement = f"COPY {table} FROM '{data_csv_path}/{table}.dat' (DELIMITER '|', HEADER, IGNORE_ERRORS);"
            f.write(statement + '\n')

        print(f"SQL file written to: {load_output_path}")

    
from enum import Enum

class Output(Enum):
    EQUAL = 0
    NEQUAL = 1
    INCONCLUSIVE = 2

def load_schema_and_data(schema, load_path):
    conn = duckdb.connect(database=':memory:')
    conn.execute(schema)
    conn.commit()

    with open(load_path, 'r') as f:
        sql = f.read()
        conn.execute(sql)
        conn.commit()
    
    return conn, schema

import subprocess

def qed(schema, orig, optimized):
    with open('tmp/temp.sql', 'w') as f:
        f.write(schema)
        f.write(orig)
        f.write("\n")
        f.write(optimized)

    cmd = ["nix", "run", "github:qed-solver/parser", "--", "../tmp"]
    subprocess.run(cmd, cwd="parser/", capture_output=False, stderr=subprocess.DEVNULL)

    cmd = ["nix", "run", "github:qed-solver/prover", "--", "../tmp"]
    result = subprocess.run(cmd,  cwd="parser/", capture_output=True, text=True)

    lines = result.stdout.splitlines()
    output = False
    for line in lines:
        if "for temp.json" in line:
            if "not provable" in line:
                qed_output = Output.NEQUAL
            elif "provable" in line:
                qed_output = Output.EQUAL
            return ("QED: " + line[:-13])

    if not output:
        qed_output = Output.INCONCLUSIVE
        return("QED: Cannot be determined")

    os.remove('tmp/temp.sql')
    return qed_output

def synthetic_data(conn, orig, optimized):
    try:
        df_orig = conn.execute(orig).fetchdf()
        df_optim = conn.execute(optimized).fetchdf()
        df_orig_sorted = df_orig.sort_values(by=df_orig.columns.tolist()).reset_index(drop=True)
        df_optim_sorted = df_optim.sort_values(by=df_optim.columns.tolist()).reset_index(drop=True)

        if df_orig_sorted.equals(df_optim_sorted):
            synthetic_output = '✅ Correct'
            print("Synthetic Data: The query results are equal")
        else:
            synthetic_output = '😵 Incorrect'
            print("Synthetic Data: The query results are not equal")
    except Exception as e:
        synthetic_output = '😵 Incorrect'
        print(e)
        print("Synthetic Data: Optimized query is not supported in DuckDB")

    return synthetic_output

# ============ FLASK APP ============
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'changeme')

TEMPLATE = '''
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>SQL Optimizer + Synthetic Check</title>
<style>body{font:14px sans-serif;} .box{max-width:700px;margin:20px auto;padding:20px;border:1px solid #ccc;}
label{display:block;margin-top:10px;}textarea{width:100%;height:80px;}button{margin:10px 0;}</style>
</head><body><div class="box">
<h1>Optimizer & Synthetic Equivalence</h1>
<form method="post" enctype="multipart/form-data">
  <label>Schema (.sql): <input type="file" name="schema" accept=".sql" required></label>
  <label>Statistics (.txt/.dat, multiple): <input type="file" name="data_files" multiple accept=".txt", ".dat"></label>
  <label>SQL Queries (.sql, multiple): <input type="file" name="query_files" multiple accept=".sql"></label>
  <label> Synthetic Data Rows: <input type="number" name="num_rows" value="100" min="1"></label>
  <label>Manual SQL Input: <textarea name="query">SELECT * FROM ...</textarea></label>
  <button name="action" value="optimize">Optimize</button>
  <button name="action" value="synthetic">Optimize + Synthetic Check</button>
</form>
{% if optimized %}
  <h2>Original Query</h2><pre>{{ user_query }}</pre>
  <h2>Optimized Query</h2><pre>{{ optimized }}</pre>
  {% if synthetic_result is not none %}
    <h2>Synthetic Equivalence</h2>
    <p>{{ synthetic_result }}</p>
    <h2>QED Equivalence</h2>
    <p>{{ QED }}</p>
    <p><a href="{{ url_for('download_data') }}">Download Generated Data</a></p>
  {% endif %}
{% endif %}
</div></body></html>'''

@app.route('/', methods=['GET','POST'])
def index():
    optimized = None
    synthetic_result = None
    user_q = ''
    qed_res = None
    if request.method=='POST':
        sch = request.files['schema']
        user_q = request.form['query'].strip()
        dfs = request.files['data_files']
        schema_sql = sch.read().decode('utf-8')
        stat = dfs.read().decode('utf-8') if dfs else ''
        opt_q = optimize_query(schema_sql, stat, user_q)
        if request.form['action']=='synthetic':
            syn_data = generate_data(schema_sql, '/tmp/data', int(request.form['num_rows']))
            qed_res = qed(schema_sql, user_q, opt_q)
            generate_copy_statements(schema_sql, '/tmp/data', '/tmp/load.sql')
            conn, schema = load_schema_and_data(schema_sql, '/tmp/load.sql')
            synthetic_result = synthetic_data(conn, user_q, opt_q)
            conn.close()
        optimized = opt_q
    return render_template_string(TEMPLATE, optimized=optimized,
                                  user_query=user_q, QED=qed_res, synthetic_result=synthetic_result)

import shutil

@app.route('/download_data')
def download_data():
    zip_path = shutil.make_archive('tmp/data', 'zip', '/tmp/data')
    return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name='data.zip')

if __name__=='__main__':
    app.run(debug=True)
