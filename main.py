import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

load_dotenv()

API_KEY = os.getenv("SM_weather") or os.getenv("OPENWEATHER_API_KEY") or os.getenv("API_KEY")

# Geocoding URL to get lat/lon from city name
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
# Forecast URL with lat/lon
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Alert Thresholds
HIGH_TEMP_THRESHOLD = 35
HIGH_HUMIDITY_THRESHOLD = 85
HIGH_WIND_THRESHOLD = 10

def get_coordinates(city_name):
    """Get latitude and longitude from city name"""
    geo_params = {
        "q": city_name,
        "appid": API_KEY
    }
    try:
        response = requests.get(GEO_URL, params=geo_params)
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"], data[0]["name"]
        return None, None, None
    except Exception as e:
        print(f"Geocoding Error: {e}")
        return None, None, None

city = input("Enter city name: ")
lat, lon, city_name = get_coordinates(city)

if not lat or not lon:
    print(f"Error: City '{city}' not found")
else:
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(FORECAST_URL, params=params)

        data = response.json()

        if response.status_code != 200:
            print("\nError:", data.get("message"))

        else:
            # Get first forecast (next 3 hours)
            first_forecast = data["list"][0]
            temperature = first_forecast["main"]["temp"]
            humidity = first_forecast["main"]["humidity"]
            weather = first_forecast["weather"][0]["description"]
            wind_speed = first_forecast["wind"]["speed"]

            print("\n===== WEATHER REPORT =====")

            print(f"City: {city_name}")
            print(f"Temperature: {temperature} °C")
            print(f"Humidity: {humidity} %")
            print(f"Weather: {weather}")
            print(f"Wind Speed: {wind_speed} m/s")

            # Alert Logic
            alerts = []

            if temperature >= HIGH_TEMP_THRESHOLD:
                alerts.append("High Temperature Alert")

            if humidity >= HIGH_HUMIDITY_THRESHOLD:
                alerts.append("High Humidity Alert")

            if wind_speed >= HIGH_WIND_THRESHOLD:
                alerts.append("High Wind Alert")

            if "rain" in weather.lower():
                alerts.append("Rain Alert")

            print("\n===== ALERT STATUS =====")

            if alerts:
                for alert in alerts:
                    print(f"⚠ {alert}")
            else:
                print("No weather alerts")

            # Create weather data dictionary
            weather_data = {
                "Temperature": [temperature],
                "Humidity": [humidity],
                "Wind Speed": [wind_speed]
            }

            # Convert to DataFrame
            df = pd.DataFrame(weather_data)

            # Create folders automatically
            os.makedirs("outputs", exist_ok=True)
            os.makedirs("images", exist_ok=True)

            # Save CSV
            csv_path = f"outputs/{city_name}_weather_report.csv"
            df.to_csv(csv_path, index=False)

            print("\nWeather report saved successfully!")
            print("CSV File:", csv_path)

            # Create Weather Visualization Chart
            plt.figure(figsize=(8, 5))

            categories = ["Temperature", "Humidity", "Wind Speed"]
            values = [temperature, humidity, wind_speed]

            plt.bar(categories, values)

            plt.title(f"Weather Report for {city_name}")
            plt.ylabel("Values")

            # Save chart
            image_path = f"images/{city_name}_weather_chart.png"

            plt.savefig(image_path)

            print("Chart saved successfully!")
            print("Chart Location:", image_path)

            plt.close()

    except Exception as e:
        print("Error:", e)