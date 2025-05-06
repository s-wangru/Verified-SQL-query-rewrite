## For shuffling schemas

```sh
cd shuffle
python schema_rewrite.py --load-sql ../dsb/queries/load_tables.sql --output-load-sql ../dsb_shuffle/load_tables.sql --schema ../dsb/queries/create_tables.sql --output-schema ../dsb_shuffle/cs.sql --dat-dir ../dsb/data --output-dat-dir ../dsb_shuffle/data 
```

```sh
python query_rewrite.py ../dsb_shuffle/cs_mapping.json ../dsb/queries/optimized_queries.txt ../dsb_shuffle/queries/cmp.txt -c
```
