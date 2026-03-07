SELECT
    date,
    city,
    month,
    DAYOFWEEK(date)                                     AS day_of_week,
    ROUND(MIN(temperature_celsius), 2)                  AS min_temp_celsius,
    ROUND(MAX(temperature_celsius), 2)                  AS max_temp_celsius,
    ROUND(AVG(temperature_celsius), 2)                  AS avg_temp_celsius,
    ROUND(SUM(precipitation), 2)                        AS total_precipitation_mm,
    SUM(CASE WHEN is_precipitation THEN 1 ELSE 0 END)   AS rainy_hours,
    SUM(CASE WHEN is_freezing THEN 1 ELSE 0 END)        AS freezing_hours,
    CASE
        WHEN AVG(temperature_celsius) < 0   THEN 'Freezing'
        WHEN AVG(temperature_celsius) < 10  THEN 'Cold'
        WHEN AVG(temperature_celsius) < 20  THEN 'Mild'
        ELSE 'Warm'
    END                                                 AS weather_category
FROM {{ ref('weather_silver') }}
GROUP BY date, city, month