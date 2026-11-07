import json
import pandas as pd

def load_raw_data(filepath="data/raw/weather_raw.json"):
    """Load the raw JSON file from disk."""
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def transform_weather_data(raw_data):
    """Clean, flatten, and standardize weather data into a pandas DataFrame."""
    all_rows = []

    # 1. Loop through each city in the raw JSON
    for city_name, city_data in raw_data.items():
        daily = city_data.get("daily", {})
        
        dates = daily.get("time", [])
        temp_max = daily.get("temperature_2m_max", [])
        temp_min = daily.get("temperature_2m_min", [])
        precipitation = daily.get("precipitation_sum", [])
        
        # 2. Combine the parallel lists into row dictionaries
        for i in range(len(dates)):
            row = {
                "city": city_name,
                "date": dates[i],
                "temp_max_c": temp_max[i],
                "temp_min_c": temp_min[i],
                "precipitation_mm": precipitation[i]
            }
            all_rows.append(row)

    # 3. Convert list of rows into a pandas DataFrame (like a table)
    df = pd.DataFrame(all_rows)

    # 4. Fix Data Types (Casting)
    df["date"] = pd.to_datetime(df["date"])
    df["temp_max_c"] = df["temp_max_c"].astype(float)
    df["temp_min_c"] = df["temp_min_c"].astype(float)
    df["precipitation_mm"] = df["precipitation_mm"].astype(float)

    # 5. Data Quality Check: Handle missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        print(f"Warning: Found {missing_count} missing values. Dropping incomplete rows...")
        df = df.dropna()
    else:
        print("Data Quality Check Passed: 0 missing values found.")

    # 6. Data Quality Check: Remove any duplicate rows
    initial_count = len(df)
    df = df.drop_duplicates(subset=["city", "date"])
    duplicates_removed = initial_count - len(df)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate records.")

    return df

if __name__ == "__main__":
    raw_data = load_raw_data()
    clean_df = transform_weather_data(raw_data)
    
    print("\n--- Cleaned DataFrame Preview (First 10 rows) ---")
    print(clean_df.head(10))
    
    print("\n--- DataFrame Column Types ---")
    print(clean_df.info())