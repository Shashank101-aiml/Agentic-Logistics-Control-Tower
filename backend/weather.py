import requests

API_KEY = "f5288b8d13c8f17310145c2ba2654d02"

def get_weather_risk(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    data = requests.get(url).json()

    temp = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    condition = data['weather'][0]['main']

    temp_c = temp - 273.15

    risk = 0
    if wind_speed > 10:
        risk += 30
    if condition in ["Rain", "Thunderstorm"]:
        risk += 50
    elif condition == "Clouds":
        risk += 10
    if humidity > 80:
        risk += 20

    return {
        "city": city,
        "temperature_c": temp_c,
        "condition": condition,
        "risk_score": min(risk, 100)
    }
if __name__ == "__main__":
    cities = ["London", "Singapore", "Dubai"]
    for city in cities:
        print(get_weather_risk(city))