SELECT
    time                                        AS observed_at,
    DATE_TRUNC('day', time)                     AS date,
    HOUR(time)                                  AS hour,
    DAYOFWEEK(time)                             AS day_of_week,
    MONTH(time)                                 AS month,
    temperature_2m                              AS temperature_celsius,
    precipitation,
    temperature_2m < 0                          AS is_freezing,
    precipitation > 0                           AS is_precipitation,
    52.52                                       AS latitude,
    13.41                                       AS longitude,
    'Berlin'                                    AS city
FROM read_parquet('s3://data-lake/bronze/data.parquet')
WHERE temperature_2m IS NOT NULL
  AND precipitation IS NOT NULL