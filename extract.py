import requests

# 1. The web address of the weather service (Open-Meteo)
URL = "https://api.open-meteo.com/v1/forecast"

# 2. What we are asking the waiter for:
# Berlin coordinates (latitude 52.52, longitude 13.41)
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    "timezone": "auto"
}

def fetch_weather():
    # Send our request over the internet
    response = requests.get(URL, params=params)
    
    # 200 means "OK / Success"
    if response.status_code == 200:
        # Convert the JSON text from the web into a Python dictionary
        data = response.json()
        return data
    else:
        print(f"Error fetching data: HTTP {response.status_code}")
        return None

if __name__ == "__main__":
    weather_data = fetch_weather()
    
    if weather_data:
        print("Successfully fetched weather data!")
        print("\nTop-level categories in the response:")
        print(list(weather_data.keys()))
        print("\nDaily weather data:")
        print(weather_data["daily"])