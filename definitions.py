import io
import subprocess

import boto3
import pandas as pd
import requests
from dagster import (
    AssetExecutionContext,
    Definitions,
    asset,
    define_asset_job,
)


@asset(group_name="bronze", compute_kind="python")
def bronze_weather_data(context: AssetExecutionContext):
    """Extract hourly weather data from Open-Meteo API and load to MinIO as Parquet (Bronze layer)."""
    API_URL = "https://archive-api.open-meteo.com/v1/archive"
    API_PARAMS = {
        "latitude": 52.52,
        "longitude": 13.41,
        "start_date": "2026-01-01",
        "end_date": "2026-01-31",
        "hourly": "temperature_2m,precipitation",
        "timezone": "Europe/Berlin",
    }

    response = requests.get(API_URL, params=API_PARAMS)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])

    buffer = io.BytesIO()
    df.to_parquet(buffer, engine="pyarrow", index=False)
    buffer.seek(0)

    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
        region_name="us-east-1",
    )
    s3.put_object(
        Bucket="data-lake",
        Key="bronze/data.parquet",
        Body=buffer,
        ContentType="application/octet-stream",
    )
    context.log.info(f"Loaded {len(df)} rows to s3://data-lake/bronze/data.parquet")


@asset(group_name="silver", deps=[bronze_weather_data], compute_kind="dbt")
def silver_weather(context: AssetExecutionContext):
    """Clean and enrich raw bronze data into the silver layer via dbt."""
    result = subprocess.run(
        [
            "dbt",
            "run",
            "--select",
            "weather_silver",
            "--project-dir",
            "/usr/app/dbt",
            "--profiles-dir",
            "/usr/app/dbt",
        ],
        capture_output=True,
        text=True,
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed:\n{result.stderr}")


@asset(group_name="gold", deps=[silver_weather], compute_kind="dbt")
def gold_weather(context: AssetExecutionContext):
    """Aggregate silver data into the gold reporting layer via dbt."""
    result = subprocess.run(
        [
            "dbt",
            "run",
            "--select",
            "weather_gold",
            "--project-dir",
            "/usr/app/dbt",
            "--profiles-dir",
            "/usr/app/dbt",
        ],
        capture_output=True,
        text=True,
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed:\n{result.stderr}")


@asset(group_name="quality", deps=[silver_weather, gold_weather], compute_kind="dbt")
def dbt_tests(context: AssetExecutionContext):
    """Run dbt tests to validate data quality across silver and gold layers."""
    result = subprocess.run(
        [
            "dbt",
            "test",
            "--project-dir",
            "/usr/app/dbt",
            "--profiles-dir",
            "/usr/app/dbt",
        ],
        capture_output=True,
        text=True,
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt test failed:\n{result.stderr}")


pipeline_job = define_asset_job(
    name="weather_pipeline",
    selection=[bronze_weather_data, silver_weather, gold_weather, dbt_tests],
)

defs = Definitions(
    assets=[bronze_weather_data, silver_weather, gold_weather, dbt_tests],
    jobs=[pipeline_job],
)
