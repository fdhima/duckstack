import requests
import pandas as pd
import logging

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

def extract_data() -> dict:
    """Extracts data from the Open-Meteo API."""
    logging.info(f"Extracting data from {API_URL}...")
    response = requests.get(API_URL, params=API_PARAMS)
    response.raise_for_status()
    data = response.json()
    logging.info("Data extracted successfully.")
    return data


def main():
    try:
        # Ingest/Extract raw data
        raw_data = extract_data()
        print(raw_data)
        
        logging.info("ETL Pipeline completed successfully.")
        
    except Exception as e:
        logging.error(f"ETL Pipeline failed: {e}")

if __name__ == "__main__":
    main()
