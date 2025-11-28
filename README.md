# 🌦️ Weather Data Pipeline (Python + SQLite)

A simple weather data pipeline built with Python.

It fetches current weather for multiple cities, stores the data in SQLite, and allows quick querying of average and latest weather records.

Includes a test script to fetch sample API data for demonstration.

## 📂 Project Structure
- weather_pipeline.py   # Main pipeline script
- test_API.py           # Test script for fetching sample API data
- weather_data.db       # SQLite database (auto-generated)
- README.md

## 🚀 Features

✅ Weather Pipeline (weather_pipeline.py)
- Fetches weather data for multiple cities (default: Colombo, London, New York, Tokyo, Sydney)
- Uses OpenWeather API (fallback to mock data if no API key)
- Saves data into weather_data.db (SQLite)
- Prints:
  - Average temperatures per city
  - Latest record for each city

### 🔹 Test API Script (test_API.py)
- Fetches JSON data from a sample API (https://jsonplaceholder.typicode.com/posts)
- Converts data to a pandas DataFrame
- Prints sample rows for testing API interaction

## 🧱 Database Structure

SQLite table: weather

| Column      | Type    | Description                       |
|------------|---------|-----------------------------------|
| city       | TEXT    | Name of the city                  |
| temperature| REAL    | Temperature in Celsius            |
| humidity   | INTEGER | Humidity percentage               |
| weather    | TEXT    | Weather description (e.g., sunny)|
| wind_speed | REAL    | Wind speed in m/s                 |
| timestamp  | TEXT    | Record timestamp (UTC)            |

## 🛠️ Installation & Setup
1️⃣ Install dependencies: pip install pandas requests python-dotenv

2️⃣ (Optional) Create a .env file for your OpenWeather API key: OPENWEATHER_API_KEY=your_api_key_here

If no API key is set, the pipeline will use mock data automatically.

## 🎯 Usage
Run the weather pipeline -> python weather_pipeline.py
- Data is appended to weather_data.db
- Average temperatures and latest records per city are printed

Run the test API script -> python test_API.py
- Fetches sample data from a placeholder API
- Prints first 5 rows of the dataset

## 🌟 Future Improvements
- Integrate with Power BI or Streamlit for dashboards
- Schedule pipeline using cron or Task Scheduler
- Add more cities and forecast data
- Store data in PostgreSQL for production
- Include data validation and alerts

## 🧑‍💻 Author
Created for learning API interaction, Python pipelines, and SQLite data storage.
