# duckstack
DuckStack: A Local-First Medallion Lakehouse

## Querying the Medallion Tables

After running the pipeline (`docker compose up`), dbt materializes the silver and gold tables into `dbt/dbt.duckdb` (persisted via the volume mount).

### Open DuckDB

```bash
docker compose run dbt duckdb /usr/app/dbt/dbt.duckdb
```

### Example queries

```sql
-- List all available tables
SHOW TABLES;

-- Inspect the silver layer (hourly, cleaned & enriched)
SELECT * FROM weather_silver LIMIT 10;

-- Inspect the gold layer (daily aggregates)
SELECT * FROM weather_gold;
```
