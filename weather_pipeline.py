#!/usr/bin/env python3
"""
weather_pipeline.py
Simple pipeline:
 - fetch current weather for a list of cities (OpenWeather)
 - save records to SQLite (append)
 - print a couple of sample queries
If no API key is set, uses mock data instead.
"""
import os
import time
import logging
from datetime import datetime
import pandas as pd
import sqlite3
from dotenv import load_dotenv

# ---- CONFIG ----
load_dotenv()  # optionally read .env file
API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = ["Colombo", "London", "New York", "Tokyo", "Sydney"]
DB_PATH = "weather_data.db"
TABLE_NAME = "weather"
REQUEST_TIMEOUT = 10
SLEEP_BETWEEN = 1.0  # avoid hammering API

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

if not API_KEY or API_KEY == "your_api_key_here":
    logging.warning("No valid API key found, running with mock data.")

# ---- FUNCTIONS ----
def fetch_weather(city: str) -> dict | None:
    # If no valid API key, return mock data
    if not API_KEY or API_KEY == "your_api_key_here":
        # Simple mock data with random-ish temps, humidity, etc.
        mock_weather = {
            "Colombo": {"temperature": 30.0, "humidity": 70, "weather": "sunny", "wind_speed": 4.5},
            "London": {"temperature": 15.5, "humidity": 80, "weather": "light rain", "wind_speed": 5.2},
            "New York": {"temperature": 20.3, "humidity": 65, "weather": "clear sky", "wind_speed": 3.1},
            "Tokyo": {"temperature": 22.0, "humidity": 60, "weather": "cloudy", "wind_speed": 6.0},
            "Sydney": {"temperature": 18.0, "humidity": 55, "weather": "windy", "wind_speed": 7.5},
        }
        data = mock_weather.get(city, {"temperature": None, "humidity": None, "weather": None, "wind_speed": None})
        return {
            "city": city,
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "weather": data["weather"],
            "wind_speed": data["wind_speed"],
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

    # Else, fetch real data
    import requests
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        main = data.get("main", {})
        weather_desc = (data.get("weather") or [{}])[0].get("description")
        wind_speed = (data.get("wind") or {}).get("speed")
        return {
            "city": city,
            "temperature": main.get("temp"),
            "humidity": main.get("humidity"),
            "weather": weather_desc,
            "wind_speed": wind_speed,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logging.warning("Failed to fetch %s: %s", city, e)
        return None

def save_to_sqlite(df: pd.DataFrame, db_path: str = DB_PATH, table: str = TABLE_NAME):
    conn = sqlite3.connect(db_path)
    df.to_sql(table, conn, if_exists="append", index=False)
    conn.close()
    logging.info("Saved %d rows to %s", len(df), db_path)

def run_sample_queries(db_path: str = DB_PATH, table: str = TABLE_NAME):
    conn = sqlite3.connect(db_path)
    q1 = f"SELECT city, ROUND(AVG(temperature),2) as avg_temp, COUNT(*) as samples FROM {table} GROUP BY city ORDER BY avg_temp DESC;"
    q2 = f'''SELECT w1.* FROM {table} w1
             INNER JOIN (SELECT city, MAX(timestamp) as maxt FROM {table} GROUP BY city) w2
             ON w1.city = w2.city AND w1.timestamp = w2.maxt;'''
    df_avg = pd.read_sql(q1, conn)
    df_latest = pd.read_sql(q2, conn)
    conn.close()
    print("\nAverage temperatures (all time):\n", df_avg)
    print("\nLatest record per city:\n", df_latest)

# ---- MAIN ----
def main():
    rows = []
    for city in CITIES:
        rec = fetch_weather(city)
        if rec:
            rows.append(rec)
        time.sleep(SLEEP_BETWEEN)
    if not rows:
        logging.error("No data fetched. Exiting.")
        return
    df = pd.DataFrame(rows)
    save_to_sqlite(df)
    run_sample_queries()

if __name__ == "__main__":
    main()
