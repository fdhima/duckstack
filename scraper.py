import requests
import pandas as pd
import logging
import io
import boto3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Define the API endpoint and parameters
API_URL = "https://archive-api.open-meteo.com/v1/archive"
API_PARAMS = {
    "latitude": 52.52,
    "longitude": 13.41,
    "start_date": "2026-01-01",
    "end_date": "2026-01-31",
    "hourly": "temperature_2m,precipitation",
    "timezone": "Europe/Berlin"
}

def extract_data() -> pd.DataFrame:
    """Extracts data from the Open-Meteo API."""
    logging.info(f"Extracting data from {API_URL}...")
    response = requests.get(API_URL, params=API_PARAMS)
    response.raise_for_status()
    data = response.json()
    hourly_data = data["hourly"]
    df = pd.DataFrame(hourly_data)
    df["time"] = pd.to_datetime(df["time"])
    return df

def load_data(df: pd.DataFrame):
    """Loads the raw data into MinIO bucket (Bronze layer)."""
    # Convert DataFrame to Parquet in memory
    buffer = io.BytesIO()
    df.to_parquet(buffer, engine="pyarrow", index=False)

    # Move buffer cursor to beginning
    buffer.seek(0)

    # Configure S3 client for MinIO
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",  # Your MinIO endpoint
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
        region_name="us-east-1"
    )

    # Upload to bucket
    s3.put_object(
        Bucket="data-lake",
        Key="processed/2026/03/03/data.parquet",
        Body=buffer,
        ContentType="application/octet-stream"
    )


def main():
    try:
        # Ingest/Extract raw data
        raw_data = extract_data()

        load_data(raw_data)                
    except Exception as e:
        print(e)
        logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
