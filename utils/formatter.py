from utils.weather import Weather

def format_weather(weather: Weather) -> str:
    """Formats weather data in string"""
    return (f"{weather.city}, температура {weather.temperature}°C, "
            f"{weather.weather_type}\n"
            f"Схід: {weather.sunrise.strftime('%H:%M')}\n"
            f"Захід: {weather.sunset.strftime('%H:%M')}\n")
