import os
import json
import requests

# Base URL for the Open-Meteo weather API
URL = "https://api.open-meteo.com/v1/forecast"

# 5 cities with their latitude and longitude coordinates
CITIES = {
    "Berlin": {"latitude": 52.52, "longitude": 13.41},
    "London": {"latitude": 51.51, "longitude": -0.13},
    "Paris": {"latitude": 48.85, "longitude": 2.35},
    "Tokyo": {"latitude": 35.68, "longitude": 139.69},
    "New York": {"latitude": 40.71, "longitude": -74.01},
}

def fetch_weather(lat, lon):
    """Fetch 7 days of daily weather metrics for given coordinates."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto"
    }
    response = requests.get(URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: HTTP {response.status_code}")
        return None

def extract_all_cities():
    """Fetch weather data for all cities in the CITIES dictionary."""
    all_weather_data = {}
    
    for city_name, coords in CITIES.items():
        print(f"Fetching weather for {city_name}...")
        data = fetch_weather(coords["latitude"], coords["longitude"])
        if data:
            all_weather_data[city_name] = data
            
    return all_weather_data

def save_raw_data(data, filepath="data/raw/weather_raw.json"):
    """Save the dictionary of raw weather data into a JSON file."""
    # Ensure the data/raw folder exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"\nRaw weather data successfully saved to: {filepath}")

if __name__ == "__main__":
    raw_data = extract_all_cities()
    save_raw_data(raw_data)