COPY (
    SELECT *
    FROM read_parquet('s3://data-lake/bronze/data.parquet')
)
TO 's3://data-lake/silver/weather.parquet'
(FORMAT PARQUET);