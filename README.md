# Verified LLM SQL Query Rewrite
**15-799 Special Topics in Databases: Query Optimization** | Spring 2025

A project that optimizes SQL queries by providing a LLM with table schema and statistics, prompting it to generate a new query, and then verifying semantic equivalence using semantic prover (QED) and running both queries on generated datasets to check for identical outputs.

## Usage

First, export your OpenAI API key with the command below.
```sh
pip install openai==0.28.1
export OPENAI_API_KEY=[your api key]
```

Run the queries below consecutively in order.
- `pipeline.py` prompts the LLM to give optimized queries by giving it the original queries, table schemas, and statistics on the table
- `generate.py` generates random tables based on the scheme given for testing query equivalence
- `test_data.py` combines the results from above and outputs whether the original query and the LLM-optimized query are equal based on the random tables generated

```sh
python pipeline.py --workload_path "dsb/queries" --schema_path "dsb/queries/create_tables.sql" --stats_path "dsb/statistics.txt"
```

```sh
python generate.py --schema_path "dsb/queries/create_tables.sql" --output_path "data"
```

```sh
python test_data.py --workload_path "dsb/queries/optimized_queries.txt" --schema_path "dsb/queries/create_tables.sql" --load_path "dsb/queries/load_tables.sql"
```