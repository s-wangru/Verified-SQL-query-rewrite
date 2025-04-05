# Verified-SQL-query-rewrite

```sh
export OPENAI_API_KEY = your api key
python pipeline.py
```

python pipeline.py --workload_path "dsb/queries" --schema_path "dsb/queries/create_tables.sql" --stats_path "dsb/queries/statistics.txt"

python generate.py --schema_path "dsb/queries/create_tables.sql" --output_path "data"

python test_data.py --workload_path "dsb/queries/optimized_queries.txt" --schema_path "dsb/queries/create_tables.sql" --load_path "dsb/queries/load_tables.sql"