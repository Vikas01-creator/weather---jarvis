import requests

API_KEY = 'd418c18a657673a4fa6d433749af9454'

def get_live_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_forecast_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        daily = {}

        for entry in data['list']:
            date = entry['dt_txt'].split(" ")[0]  # "2026-02-27"
            time = entry['dt_txt'].split(" ")[1]  # "12:00:00"

            # Pick the 12:00 reading as the daily representative
            if date not in daily or time == "12:00:00":
                daily[date] = {
                    "time": date,
                    "temp": round(entry['main']['temp'], 2),
                    "wind": entry['wind']['speed']
                }

        return list(daily.values())[:7]  # ✅ exactly 7 days
    return None