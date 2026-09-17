memory = []
import requests
 
def calculator(expression):
    allowed = set("0123456789+-*/.() ")
    if not set(expression) <= allowed:
        return "Invalid calculation"
    return str(eval(expression, {"__builtins__": {}}, {}))
 
def weather(city):
    try:
        place = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en"},
            timeout=10
        ).json()["results"][0]
 
        data = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "timezone": "auto"
            },
            timeout=10
        ).json()["current"]
 
        return (f"Live weather in {place['name']}: {data['temperature_2m']}°C, "
                f"humidity {data['relative_humidity_2m']}%, "
                f"wind {data['wind_speed_10m']} km/h, "
                f"weather code {data['weather_code']}.")
    except Exception as error:
        return f"Weather service error: {error}"