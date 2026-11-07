import os
import sqlite3

DB_PATH = "data/weather.db"

def init_database():
    """Create the SQLite database and define the tables."""
    # Ensure the data/ directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Connect to SQLite (creates data/weather.db file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create the 'cities' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        city_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT NOT NULL UNIQUE,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    );
    """)

    # 2. Create the 'weather_daily' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_daily (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        temp_max_c REAL NOT NULL,
        temp_min_c REAL NOT NULL,
        precipitation_mm REAL NOT NULL,
        FOREIGN KEY (city_id) REFERENCES cities (city_id),
        UNIQUE (city_id, date) -- Prevents duplicate entries for the same city and date!
    );
    """)

    conn.commit()
    conn.close()
    print(f"Database successfully created at: {DB_PATH}")

if __name__ == "__main__":
    init_database()