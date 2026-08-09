"""
Basic Weather App
Oasis Infobyte AICTE SIP - Python Programming Track - Task 4

Asks the user for a city name, fetches current weather data from the
OpenWeatherMap API, and displays temperature, humidity, condition,
and wind speed.
"""

import requests

# Paste your free OpenWeatherMap API key between the quotes below.
# Get one at: https://openweathermap.org/ (My API Keys, after signing up)
API_KEY = "API_KEY_HERE"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_city():
    """Keeps asking until the user enters a non-empty city name."""
    while True:
        city = input("Enter a city name: ").strip()
        if not city:
            print("Error: City name cannot be empty. Please try again.")
            continue
        return city


def celsius_to_fahrenheit(celsius):
    """Converts a Celsius temperature to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def fetch_weather(city, api_key):
    """
    Calls the OpenWeatherMap API for the given city.
    Returns a dict with the parsed weather data.
    Raises a ValueError with a clear message if anything goes wrong.
    """
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        raise ValueError("Could not connect to the internet. Please check your connection.")
    except requests.exceptions.Timeout:
        raise ValueError("The request timed out. Please try again.")

    if response.status_code == 401:
        raise ValueError("Invalid API key. Note: new keys can take up to 2 hours to activate.")
    if response.status_code == 404:
        raise ValueError(f"City '{city}' not found. Please check the spelling and try again.")
    if response.status_code != 200:
        raise ValueError(f"Unexpected error from weather service (status code {response.status_code}).")

    data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp_c": data["main"]["temp"],
        "temp_f": celsius_to_fahrenheit(data["main"]["temp"]),
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].capitalize(),
        "wind_speed": data["wind"]["speed"],
    }


def display_weather(weather):
    """Prints the weather data in a clean, readable format."""
    print(f"\n--- Weather in {weather['city']}, {weather['country']} ---")
    print(f"Temperature: {weather['temp_c']:.1f}°C ({weather['temp_f']:.1f}°F)")
    print(f"Condition: {weather['description']}")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Wind Speed: {weather['wind_speed']} m/s")


def main():
    print("=== Basic Weather App ===")
    print("This tool shows current weather conditions for any city.\n")

    if API_KEY == "YOUR_API_KEY_HERE":
        print("Error: Please add your OpenWeatherMap API key at the top of this file "
              "before running the app.")
        return

    while True:
        city = get_city()
        try:
            weather = fetch_weather(city, API_KEY)
            display_weather(weather)
        except ValueError as e:
            print(f"Error: {e}")

        again = input("\nCheck another city? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
