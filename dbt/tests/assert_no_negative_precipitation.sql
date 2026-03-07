SELECT *
FROM {{ ref('weather_silver') }}
WHERE precipitation < 0
