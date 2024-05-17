from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/weather", methods=["GET", "POST"])
def get_weather():
    try:
        latitude = request.args.get("lat")
        longitude = request.args.get("lon")
        city = request.form.get("city")

        if latitude and longitude:
            location = f"{latitude},{longitude}"
            place_name = get_place_name(latitude, longitude)
        elif city:
            location = city
            place_name = city
        else:
            location = "London"  # default location
            place_name = "London"

        weather_data = get_weather_data(
            place_name
        )  # Use place_name to fetch weather data

        if request.method == "GET":
            return jsonify(
                html=render_template(
                    "weather_data.html", weather=weather_data, city=place_name
                )
            )
        else:
            return render_template("index.html", weather=weather_data, city=place_name)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500


def get_place_name(latitude, longitude):
    try:
        openweather_key = os.getenv("OPENWEATHER_KEY")
        geocode_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit=1&appid={openweather_key}"
        response = requests.get(geocode_url).json()
        app.logger.info(f"Geocode response: {response}")
        if response and isinstance(response, list) and len(response) > 0:
            return response[0].get("name", "Unknown location")
        return "Unknown location"
    except Exception as e:
        app.logger.error(f"Error in get_place_name: {e}")
        return "Unknown location"


def get_weather_data(city):
    try:
        weather_data = {}

        weatherapi_key = os.getenv("WEATHERAPI_KEY")
        openweather_key = os.getenv("OPENWEATHER_KEY")

        # Get current weather and 24-hour forecast from WeatherAPI
        weatherapi_current_url = (
            f"http://api.weatherapi.com/v1/current.json?key={weatherapi_key}&q={city}"
        )
        weatherapi_forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={weatherapi_key}&q={city}&days=1"

        weatherapi_current_response = requests.get(weatherapi_current_url).json()
        weatherapi_forecast_response = requests.get(weatherapi_forecast_url).json()

        weather_data["WeatherAPI"] = {
            "current": {
                "temperature": weatherapi_current_response["current"]["temp_c"],
                "condition": weatherapi_current_response["current"]["condition"][
                    "text"
                ],
                "icon": weatherapi_current_response["current"]["condition"]["icon"],
                "humidity": weatherapi_current_response["current"]["humidity"],
                "wind_speed": weatherapi_current_response["current"]["wind_kph"],
                "feels_like": weatherapi_current_response["current"]["feelslike_c"],
                "visibility": weatherapi_current_response["current"]["vis_km"],
                "uv_index": weatherapi_current_response["current"]["uv"],
                "pressure": weatherapi_current_response["current"]["pressure_mb"],
                "cloud": weatherapi_current_response["current"]["cloud"],
                "date_time": datetime.strptime(
                    weatherapi_current_response["location"]["localtime"],
                    "%Y-%m-%d %H:%M",
                ).strftime("%d/%m/%Y %H:%M"),
            },
            "forecast": [
                {
                    "time": datetime.strptime(hour["time"], "%Y-%m-%d %H:%M").strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                    "temperature": hour["temp_c"],
                    "condition": hour["condition"]["text"],
                    "icon": hour["condition"]["icon"],
                    "humidity": hour["humidity"],
                    "wind_speed": hour["wind_kph"],
                    "feels_like": hour["feelslike_c"],
                    "visibility": hour["vis_km"],
                    "uv_index": hour["uv"],
                    "pressure": hour["pressure_mb"],
                    "cloud": hour["cloud"],
                }
                for hour in weatherapi_forecast_response.get("forecast", {})
                .get("forecastday", [])[0]
                .get("hour", [])
            ],
        }

        # Get 5-day weather forecast from OpenWeatherAPI
        openweather_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={openweather_key}&units=metric"
        openweather_response = requests.get(openweather_url).json()

        openweather_forecast = []
        if "list" in openweather_response:
            forecast_entries = openweather_response["list"]
            daily_forecasts = {}

            for entry in forecast_entries:
                date = entry["dt_txt"].split(" ")[0]
                if date not in daily_forecasts:
                    daily_forecasts[date] = entry
                else:
                    existing_hour = int(
                        daily_forecasts[date]["dt_txt"].split(" ")[1].split(":")[0]
                    )
                    current_hour = int(entry["dt_txt"].split(" ")[1].split(":")[0])
                    if abs(current_hour - 12) < abs(existing_hour - 12):
                        daily_forecasts[date] = entry

            openweather_forecast = [
                {
                    "date": datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y"),
                    "temperature": entry["main"]["temp"],
                    "condition": entry["weather"][0]["description"],
                    "icon": f"http://openweathermap.org/img/wn/{entry['weather'][0]['icon']}@2x.png",
                    "humidity": entry["main"]["humidity"],
                    "wind_speed": entry["wind"]["speed"],
                    "feels_like": entry["main"]["feels_like"],
                    "visibility": entry.get("visibility", 0)
                    / 1000,  # convert meters to kilometers
                    "pressure": entry["main"]["pressure"],
                    "cloud": entry["clouds"]["all"],
                }
                for date, entry in sorted(daily_forecasts.items())
            ]

        weather_data["OpenWeatherAPI"] = {
            "forecast": openweather_forecast,
        }

        return weather_data
    except Exception as e:
        app.logger.error(f"Error in get_weather_data: {e}")
        return {}


if __name__ == "__main__":
    app.run(debug=True)
