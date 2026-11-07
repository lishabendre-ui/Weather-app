import time
import logging
import sys
from create_db import init_database
from extract import extract_all_cities, save_raw_data
from transform import load_raw_data, transform_weather_data
from load import get_connection, load_cities, load_weather_data

# Configure logging: outputs to both the terminal and 'pipeline.log'
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_pipeline():
    """Run the complete Weather Data Pipeline with logging and error handling."""
    start_time = time.time()
    logging.info("==================================================")
    logging.info("🌤️  WEATHER DATA PIPELINE STARTED")
    logging.info("==================================================")

    try:
        # Step 1: Database Setup
        logging.info("Step 1/4: Initializing SQLite database schema...")
        init_database()

        # Step 2: Extract Phase
        logging.info("Step 2/4: Extracting weather data from Open-Meteo API...")
        raw_data = extract_all_cities()
        if not raw_data:
            raise ValueError("Extraction returned no data!")
        save_raw_data(raw_data)

        # Step 3: Transform Phase
        logging.info("Step 3/4: Transforming and validating data with pandas...")
        raw_json = load_raw_data()
        clean_df = transform_weather_data(raw_json)
        logging.info(f"Transform complete: {len(clean_df)} clean records prepared.")

        # Step 4: Load Phase
        logging.info("Step 4/4: Loading clean records into SQLite database...")
        conn = get_connection()
        load_cities(conn)
        load_weather_data(conn, clean_df)

        # Verify final record count
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather_daily;")
        total_records = cursor.fetchone()[0]
        conn.close()

        elapsed = round(time.time() - start_time, 2)
        logging.info("==================================================")
        logging.info(f"✅ PIPELINE COMPLETED SUCCESSFULLY in {elapsed}s")
        logging.info(f"📊 Total records in database: {total_records}")
        logging.info("==================================================")

    except Exception as e:
        logging.error(f"❌ Pipeline failed with error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()