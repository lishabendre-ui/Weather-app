import unittest
import sqlite3
import pandas as pd
from transform import transform_weather_data

class TestWeatherPipeline(unittest.TestCase):
    
    def setUp(self):
        """Set up dummy raw API data for testing."""
        self.mock_raw_data = {
            "TestCity": {
                "daily": {
                    "time": ["2026-11-01", "2026-11-02"],
                    "temperature_2m_max": [15.5, 18.2],
                    "temperature_2m_min": [8.0, 9.5],
                    "precipitation_sum": [0.0, 2.4]
                }
            }
        }

    def test_transform_output_structure(self):
        """Test that transform produces the correct DataFrame columns and row count."""
        df = transform_weather_data(self.mock_raw_data)
        
        # 1. Check that 2 rows were processed
        self.assertEqual(len(df), 2)
        
        # 2. Check that all expected columns exist
        expected_columns = {"city", "date", "temp_max_c", "temp_min_c", "precipitation_mm"}
        self.assertTrue(expected_columns.issubset(df.columns))
        
        # 3. Check data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["date"]))
        self.assertTrue(pd.api.types.is_float_dtype(df["temp_max_c"]))
        
        # 4. Check that there are zero null values
        self.assertEqual(df.isnull().sum().sum(), 0)

    def test_idempotent_database_constraint(self):
        """Test that the database enforces UNIQUE(city_id, date) and avoids duplicates."""
        # Create an in-memory SQLite database for testing
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # Create minimal table with unique constraint
        cursor.execute("""
        CREATE TABLE weather_test (
            city_id INTEGER,
            date TEXT,
            temp_max REAL,
            UNIQUE(city_id, date)
        );
        """)
        
        # Insert a record
        cursor.execute("INSERT OR REPLACE INTO weather_test VALUES (1, '2026-11-01', 15.5);")
        
        # Insert the exact same record again with an updated temperature
        cursor.execute("INSERT OR REPLACE INTO weather_test VALUES (1, '2026-11-01', 16.0);")
        conn.commit()
        
        # Verify row count is still 1, NOT 2!
        cursor.execute("SELECT COUNT(*), temp_max FROM weather_test;")
        count, temp = cursor.fetchone()
        
        self.assertEqual(count, 1)
        self.assertEqual(temp, 16.0)
        conn.close()

if __name__ == "__main__":
    unittest.main()