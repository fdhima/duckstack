COPY (
    SELECT *
    FROM read_parquet('s3://data-lake/silver/weather.parquet')
)
TO 's3://data-lake/gold/weather.parquet'
(FORMAT PARQUET);