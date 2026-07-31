# Basic Weather App

**Oasis Infobyte AICTE SIP — Python Programming Track — Task 4**

## What This Project Does

This is a command-line program that fetches and displays real-time weather
data for any city using the free OpenWeatherMap API. Just type a city name
and get the current temperature, humidity, condition, and wind speed.

## Features

- Asks for a city name (or ZIP code)
- Fetches live weather data from OpenWeatherMap API
- Displays temperature in both Celsius and Fahrenheit
- Shows humidity percentage, weather condition description, and wind speed
- Handles errors gracefully: city not found, invalid API key, network issues,
  timeouts — each with a clear, helpful message instead of crashing
- Rejects empty city input with validation
- Lets you check multiple cities in one session without restarting

## How to Run

1. Get a free API key:
   - Go to **openweathermap.org**
   - Sign up (free account)
   - Go to **My API Keys** and copy your default key
   - **Note:** New keys can take 10 minutes to 2 hours to activate

2. Open `weather_app.py` in a text editor and find this line near the top:
   ```python
   API_KEY = "YOUR_API_KEY_HERE"
   ```
   Replace `YOUR_API_KEY_HERE` with your actual API key (keep the quotes)

3. Open a terminal in this folder and run:
   ```
   python weather_app.py
   ```

4. Enter a city name when prompted and see the weather!

## Example

```
=== Basic Weather App ===
This tool shows current weather conditions for any city.

Enter a city name: Lahore

--- Weather in Lahore, PK ---
Temperature: 34.5°C (94.1°F)
Condition: Clear sky
Humidity: 40%
Wind Speed: 3.2 m/s

Check another city? (yes/no): yes

Enter a city name: London

--- Weather in London, GB ---
Temperature: 18.2°C (64.8°F)
Condition: Partly cloudy
Humidity: 65%
Wind Speed: 5.1 m/s

Check another city? (yes/no): no
Goodbye!
```

## Technologies Used

- Python 3 (standard library: `requests` module for API calls)
- OpenWeatherMap API (free tier)
- JSON parsing

## What I Learned

Building this project helped me practice:
- Making HTTP requests to real APIs
- Parsing JSON responses
- Converting between temperature units
- Handling multiple types of errors (network, API, user input) gracefully
- Writing clear error messages instead of letting exceptions crash the program
