import sqlite3
import pandas as pd
from extract import CITIES
from transform import load_raw_data, transform_weather_data

DB_PATH = "data/weather.db"

def get_connection():
    """Connect to SQLite database with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def load_cities(conn):
    """Insert cities into the 'cities' table idempotently."""
    cursor = conn.cursor()
    
    for city_name, coords in CITIES.items():
        # INSERT OR IGNORE skips the row if city_name already exists
        cursor.execute("""
        INSERT OR IGNORE INTO cities (city_name, latitude, longitude)
        VALUES (?, ?, ?);
        """, (city_name, coords["latitude"], coords["longitude"]))
        
    conn.commit()
    print("Cities loaded successfully.")

def get_city_id_map(conn):
    """Fetch a dictionary mapping city_name -> city_id from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT city_id, city_name FROM cities;")
    rows = cursor.fetchall()
    return {city_name: city_id for city_id, city_name in rows}

def load_weather_data(conn, df):
    """Insert cleaned DataFrame records into 'weather_daily' idempotently."""
    cursor = conn.cursor()
    
    # 1. Get the city_id for each city
    city_map = get_city_id_map(conn)
    
    # 2. Add city_id column to the DataFrame
    df["city_id"] = df["city"].map(city_map)
    
    # 3. Insert each row into weather_daily
    # INSERT OR REPLACE updates the record if (city_id, date) already exists
    insert_sql = """
    INSERT OR REPLACE INTO weather_daily (city_id, date, temp_max_c, temp_min_c, precipitation_mm)
    VALUES (?, ?, ?, ?, ?);
    """
    
    records = []
    for _, row in df.iterrows():
        date_str = row["date"].strftime("%Y-%m-%d")
        records.append((
            int(row["city_id"]),
            date_str,
            float(row["temp_max_c"]),
            float(row["temp_min_c"]),
            float(row["precipitation_mm"])
        ))
        
    cursor.executemany(insert_sql, records)
    conn.commit()
    print(f"Loaded {len(records)} weather records into 'weather_daily'.")

if __name__ == "__main__":
    conn = get_connection()
    
    # 1. Load cities
    load_cities(conn)
    
    # 2. Extract & Transform data
    raw_data = load_raw_data()
    clean_df = transform_weather_data(raw_data)
    
    # 3. Load weather data into SQLite
    load_weather_data(conn, clean_df)
    
    # 4. Check total counts in the database
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cities;")
    cities_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM weather_daily;")
    weather_count = cursor.fetchone()[0]
    
    print(f"\n--- Database Summary ---")
    print(f"Total Cities: {cities_count}")
    print(f"Total Weather Records: {weather_count}")
    
    conn.close()