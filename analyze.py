import sqlite3
import pandas as pd

DB_PATH = "data/weather.db"

def run_query(query, title):
    """Execute a SQL query and print the result using pandas for nice formatting."""
    conn = sqlite3.connect(DB_PATH)
    print(f"\n{'='*20} {title} {'='*20}")
    
    # pandas read_sql_query runs the query and formats results as a clean table
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    conn.close()

def main():
    # Query 1: Average temperatures and total rain per city
    query1 = """
    SELECT 
        c.city_name,
        ROUND(AVG(w.temp_max_c), 1) AS avg_max_temp_c,
        ROUND(AVG(w.temp_min_c), 1) AS avg_min_temp_c,
        ROUND(SUM(w.precipitation_mm), 1) AS total_rain_mm
    FROM cities c
    JOIN weather_daily w ON c.city_id = w.city_id
    GROUP BY c.city_name
    ORDER BY avg_max_temp_c DESC;
    """
    run_query(query1, "1. Weekly Summary per City")

    # Query 2: The hottest day recorded for each city
    query2 = """
    SELECT 
        c.city_name,
        w.date,
        w.temp_max_c AS max_temp_c
    FROM cities c
    JOIN weather_daily w ON c.city_id = w.city_id
    WHERE (w.city_id, w.temp_max_c) IN (
        SELECT city_id, MAX(temp_max_c)
        FROM weather_daily
        GROUP BY city_id
    )
    ORDER BY max_temp_c DESC;
    """
    run_query(query2, "2. Hottest Day per City")

    # Query 3: The wettest day across all cities
    query3 = """
    SELECT 
        c.city_name,
        w.date,
        w.precipitation_mm
    FROM cities c
    JOIN weather_daily w ON c.city_id = w.city_id
    ORDER BY w.precipitation_mm DESC
    LIMIT 1;
    """
    run_query(query3, "3. Single Wettest Day Overall")

    # Query 4: Top 3 warmest days overall across all cities
    query4 = """
    SELECT 
        c.city_name,
        w.date,
        w.temp_max_c
    FROM cities c
    JOIN weather_daily w ON c.city_id = w.city_id
    ORDER BY w.temp_max_c DESC
    LIMIT 3;
    """
    run_query(query4, "4. Top 3 Warmest Days Overall")

if __name__ == "__main__":
    main()