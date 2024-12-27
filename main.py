import logging
import logging.handlers
import os
import requests

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# Fetch secret from environment variable with logging
try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    logger.warning("SOME_SECRET environment variable is not set.")

def fetch_weather_data(city, country):
    """
    Fetch weather data for a given city and country.

    Args:
        city (str): City name.
        country (str): Country code.
    
    Returns:
        dict: Parsed weather data or None if request failed.
    """
    url = f'https://weather.talkpython.fm/api/weather/?city={city}&country={country}'
    
    try:
        logger.info(f"Requesting weather data for {city}, {country}")
        response = requests.get(url)
        
        # Log status code and response text for debugging
        logger.debug(f"HTTP Status Code: {response.status_code}")
        if response.status_code != 200:
            logger.error(f"Failed to fetch weather data: {response.text}")
            return None
        
        data = response.json()
        return data

    except requests.RequestException as e:
        # Log any network-related errors
        logger.error(f"Error during API request: {e}")
        return None

if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")
    
    # Fetch weather data
    city = "Berlin"
    country = "DE"
    weather_data = fetch_weather_data(city, country)

    if weather_data:
        # If data exists, extract and log the temperature
        try:
            temperature = weather_data["forecast"]["temp"]
            logger.info(f'Weather in {city}: {temperature}°C')
        except KeyError:
            logger.error("Error: 'forecast' or 'temp' not found in the response data.")
    else:
        logger.error("Weather data retrieval failed.")
