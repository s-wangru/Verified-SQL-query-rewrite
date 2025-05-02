# Shuffling schemas

This takes a list of words and randomly replaces the table and column names with these words. The code below can rewrite the schema, dataset, and queries.

```sh
cd shuffle
```

```sh
python schema_rewrite.py --load-sql ../dsb/queries/load_tables.sql --output-load-sql ../dsb_shuffle/load_tables.sql --schema ../dsb/queries/create_tables.sql --output-schema ../dsb_shuffle/create_tables.sql --dat-dir ../dsb/data --output-dat-dir ../dsb_shuffle/data
```

```sh
python query_rewrite.py ../dsb_shuffle/create_tables_mapping.json ../dsb/queries ../dsb_shuffle/queries -c
```
