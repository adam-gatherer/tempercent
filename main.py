import requests
from datetime import timedelta, date


def longlat_from_postcode(postcode: str):
    URL = "https://api.postcodes.io/postcodes/" + postcode
    r = requests.get(url=URL)
    data = (r.json())
    long = data['result']['longitude']
    lat = data['result']['latitude']
    return float(long), float(lat)


def get_past_five_years():
    five_years = []
    date_today = date.today()
    for i in range(1, 6):
        five_years.append(date_today - timedelta(days=i * 365))
    return five_years


def get_avg_five_years(longitude: float, latitude: float, today, timezone):
    start_date = today - timedelta(days=5 * 365)
    end_date = today
    URL = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max&timezone={timezone}"
    r = requests.get(url=URL)
    data = r.json()
    dates = data['daily']['time']
    temps = data['daily']['temperature_2m_max']
    last_five_temps = []
    for i in get_past_five_years():
        index = dates.index(str(i))
        last_five_temps.append(temps[index])
    return round((sum(last_five_temps) / len(last_five_temps)), 2)


def get_temp_today(longitude: float, latitude: float, today, timezone):
    URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max&current_weather=true&timezone={timezone}"
    r = requests.get(url=URL)
    data = r.json()
    return data['current_weather']['temperature']


longitude, latitude = longlat_from_postcode("EH51EZ")
today = date.today()
timezone = "GMT"
avg_five_years = get_avg_five_years(longitude, latitude, today, timezone)
temp_today = get_temp_today(longitude, latitude, today, timezone)
today_pct = int(round(temp_today / avg_five_years, 2) * 100)
if today_pct > 100:
    today_pct -= 100
    above_below = "above"
else:
    above_below = "below"
print(f'Today is {today_pct}% {above_below} the average temperature over the past five years.')
