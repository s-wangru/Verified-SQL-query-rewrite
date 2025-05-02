# Verified LLM SQL Query Rewrite
**15-799 Special Topics in Databases: Query Optimization** | Spring 2025

A project that optimizes SQL queries by providing a LLM with table schema and statistics, prompting it to generate a new query, and then verifying semantic equivalence using semantic prover and running both queries on generated datasets to check for identical outputs.

It utilizes the parser and prover in [Query Equivalence Decider (QED)](https://github.com/qed-solver) to perform the semantic equivalence check.

## Usage
After cloning this project, include the submodules (prover & parser):
```sh
git submodule update --init --recursive
```

Export your OpenAI API key:
```sh
export OPENAI_API_KEY=[your api key]
```

Install the necessary packages:
```sh
pip install openai==0.28.1 faker duckdb
curl -L https://nixos.org/nix/install | sh
```

Restart the terminal & run the commands below consecutively in order.
- `prompt_llm.py` prompts the LLM to give optimized queries by giving it the original queries, table schemas, and statistics on the table
- `generate_data.py` generates random tables based on the scheme given for testing query equivalence
- `check_equivalence.py` combines the results from above and outputs whether the original query and the LLM-optimized query are equal based on QED & the random tables generated

```sh
python prompt_llm.py --workload_path "dsb/queries" --schema_path "dsb/queries/create_tables.sql" --stats_path "dsb/statistics.txt"
```

```sh
python generate_data.py --schema_path "dsb/queries/create_tables.sql" --data_output_path "data"
```

```sh
python check_equivalence.py --workload_path "dsb/queries/optimized_queries.txt" --schema_path "dsb/queries/create_tables.sql" --load_path "dsb/queries/load_tables.sql"
```

## Shuffle Schemas

This is for benchmarking usage to determine whether the LLM's performance is due to it having seen the queries before (possibility for more comon benchmarks like TPC-H, TPC-DS, etc.) or it actually has the ability to rewrite the query. Refer to `shuffle` folder's documentation for how to use.

## Tests & Code Coverage
Install the necessary packages:
```sh
pip install pytest pytest-cov pandas
```

To run all unit tests & check code coverage:
```sh
pytest --cov=. --cov-config=.coveragerc
```