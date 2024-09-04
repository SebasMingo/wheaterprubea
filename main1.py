import requests
import argparse
import pyfiglet
from simple_chalk import chalk
import json

# API Key y URL base de la API
API_KEY = '4f94042cbebb59e07feaa6527b71b136'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Mapeo de íconos del clima
WEATHER_ICONS = {
    "01d": "☀️", "02d": "⛅️", "03d": "☁️", "04d": "☁️",
    "09d": "🌧", "10d": "🌦", "11d": "⛈", "13d": "🌨", "50d": "🌫",
    "01n": "🌙", "02n": "☁️", "03n": "☁️", "04n": "☁️",
    "09n": "🌧", "10n": "🌦", "11n": "⛈", "13n": "🌨", "50n": "🌫",
}

def get_weather_data(country):
    url = f"{BASE_URL}?q={country}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 404:
        print(chalk.red(f"Error: City '{country}' not found."))
        return None
    elif response.status_code == 401:
        print(chalk.red("Error: Invalid API Key."))
        return None
    elif response.status_code != 200:
        print(chalk.red(f"Error: Unable to retrieve weather information for '{country}'."))
        return None

    return response.json()

def display_weather(data, format="text"):
    if not data:
        return

    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]
    city = data["name"]
    country = data["sys"]["country"]

    if format == "json":
        print(json.dumps(data, indent=4))
    elif format == "csv":
        print(f"{city},{country},{temperature},{feels_like},{description}")
    else:
        weather_icon = WEATHER_ICONS.get(icon, "")
        output = f"{pyfiglet.figlet_format(city)}, {country}\n\n"
        output += f"{weather_icon} {description}\n"
        output += f"Temperature: {temperature}°C\n"
        output += f"Feels like: {feels_like}°C\n"
        print(chalk.green(output))

def main():
    parser = argparse.ArgumentParser(description="Check the weather for a certain country/city.")
    parser.add_argument("countries", nargs="+", help="the countries/cities to check the weather for")
    parser.add_argument("--format", choices=["json", "csv", "text"], default="text", help="Output format")
    args = parser.parse_args()

    for country in args.countries:
        data = get_weather_data(country)
        display_weather(data, args.format)

if __name__ == "__main__":
    main()
