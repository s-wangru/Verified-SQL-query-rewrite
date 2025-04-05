# Verified-SQL-query-rewrite

```sh
export OPENAI_API_KEY = your api key
```

```sh
python pipeline.py --workload_path "dsb/queries" --schema_path "dsb/queries/create_tables.sql" --stats_path "dsb/statistics.txt"
```

```sh
python generate.py --schema_path "dsb/queries/create_tables.sql" --output_path "data"
```

```sh
python test_data.py --workload_path "dsb/queries/optimized_queries.txt" --schema_path "dsb/queries/create_tables.sql" --load_path "dsb/queries/load_tables.sql"
```