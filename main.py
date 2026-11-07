import time
from datetime import datetime
from create_db import init_database
from extract import extract_all_cities, save_raw_data
from transform import load_raw_data, transform_weather_data
from load import get_connection, load_cities, load_weather_data

def run_pipeline():
    """Run the complete Weather Data Pipeline end to end."""
    start_time = time.time()
    print("=" * 60)
    print(f" Weather Pipeline Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Initialize Database Schema
    print("\n[Step 1/4] Initializing Database Schema...")
    init_database()

    # 2. Extract Phase
    print("\n[Step 2/4] Extracting Weather Data from Open-Meteo API...")
    raw_data = extract_all_cities()
    save_raw_data(raw_data)

    # 3. Transform Phase
    print("\n[Step 3/4] Transforming and Validating Data with pandas...")
    raw_data = load_raw_data()
    clean_df = transform_weather_data(raw_data)
    print(f"Successfully cleaned {len(clean_df)} weather records.")

    # 4. Load Phase
    print("\n[Step 4/4] Loading Cleaned Records into SQLite...")
    conn = get_connection()
    load_cities(conn)
    load_weather_data(conn, clean_df)

    # Verification Query
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM weather_daily;")
    total_records = cursor.fetchone()[0]
    conn.close()

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 60)
    print(f" Pipeline Finished Successfully in {elapsed} seconds!")
    print(f" Total Records in Database: {total_records}")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()