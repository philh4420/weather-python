# Flask Weather App

This Flask application fetches and displays weather data for a given location using the WeatherAPI and OpenWeatherAPI. The application can determine the user's current location using the browser's Geolocation API and display weather information for that location on page load.

## Features

- Fetch current weather data and 24-hour forecast from WeatherAPI.
- Fetch 5-day weather forecast from OpenWeatherAPI.
- Display weather data for the user's current location or a specified city.

## Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/weather-app.git
    cd weather-app
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root directory and add your API keys. You can use the provided `.env_dummy` file as a template:

    ```bash
    cp .env_dummy .env
    ```

    Open the `.env` file in a text editor and replace the placeholders with your actual API keys:

    ```plaintext
    WEATHERAPI_KEY=your_weatherapi_key
    OPENWEATHER_KEY=your_openweather_key
    ```

## Usage

1. Run the Flask application:

    ```bash
    flask run
    ```

2. Open your web browser and navigate to `http://localhost:5000` to use the application.

## File Structure
weather-app/
│
├── app.py
├── requirements.txt
├── .env_dummy
├── README.md
├── static/
│ ├── script.js
│ └── styles.css
├── templates/
│ ├── index.html
│ └── weather_data.html
└── venv/


## API Configuration

The application uses two external APIs: WeatherAPI and OpenWeatherAPI. You need to sign up on their respective websites to get API keys:

- [WeatherAPI](https://www.weatherapi.com/)
- [OpenWeatherAPI](https://openweathermap.org/api)

Once you have the API keys, update your `.env` file with the keys as shown above.

## Explanation of .env

1. Create `.env`:

2. Edit the `.env` file and replace the placeholders with your actual API keys:

    ```plaintext
    WEATHERAPI_KEY=your_weatherapi_key
    OPENWEATHER_KEY=your_openweather_key
    ```

This will ensure that your API keys are loaded as environment variables and used securely by the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [WeatherAPI](https://www.weatherapi.com/)
- [OpenWeatherAPI](https://openweathermap.org/api)
- [Flask](https://flask.palletsprojects.com/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)


