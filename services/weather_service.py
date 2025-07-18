import requests

API_KEY = "YOUR_OPENWEATHER_KEY"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"]
        }
    return {"city": city, "temp": "N/A", "desc": "No data"}