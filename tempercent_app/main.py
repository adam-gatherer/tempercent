import requests
from datetime import timedelta, date
from timezonefinder import TimezoneFinder
from ukpostcodeutils import validation

tf = TimezoneFinder()

def longlat_from_postcode(postcode: str) -> tuple[float, float]:
    # postcode = "BEPIS"
    URL = "https://api.postcodes.io/postcodes/" + postcode
    r = requests.get(url=URL)
    data = r.json()
    if r.status_code == 200:
        long = data['result']['longitude']
        lat = data['result']['latitude']
        return float(long), float(lat)
    else:
        raise Exception(f'Postcodes.io error: {r.status_code}')
            
       
def get_past_five_years() -> list:
    five_years = []
    date_today = date.today()
    for i in range(1, 6):
        five_years.append(date_today - timedelta(days=i * 365))
    return five_years


def get_avg_five_years(longitude: float, latitude: float, today: date, timezone: str) -> float:
    start_date = today - timedelta(days=5 * 365)
    end_date = today
    payload = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': start_date,
        'end_date': end_date,
        'daily': 'temperature_2m_max',
        'timezone': timezone
        
    }
    r = requests.get("https://archive-api.open-meteo.com/v1/archive", params=payload)
    data = r.json()
    if r.status_code == 200:
        dates = data['daily']['time']
        temps = data['daily']['temperature_2m_max']
        last_five_temps = []
        for i in get_past_five_years():
            index = dates.index(str(i))
            last_five_temps.append(temps[index])
        return round((sum(last_five_temps) / len(last_five_temps)), 2)
    else:
        raise Exception(f'Open-Meteo error: {r.status_code}, {data["error"]}')


def get_temp_today(longitude: float, latitude: float, today: date, timezone: str) -> float:
    payload = {
        'latitude': latitude,
        'longitude': longitude,
        'daily': 'temperature_2m_max',
        'current_weather': 'true',
        'timezone': timezone
    }
    r = requests.get('https://api.open-meteo.com/v1/forecast', params=payload)
    data = r.json()
    if r.status_code == 200:
        return data['current_weather']['temperature']
    else:
        raise Exception(f'Open-Meteo error: {r.status_code}, {data["error"]}')

def main_function(postcode: str) -> dict:
    postcode = (postcode.replace(" ", "")).upper()
    if not validation.is_valid_postcode(postcode):
        return f'Postcode "{postcode}" invalid.'
    longitude, latitude = longlat_from_postcode(postcode)
    today = date.today()
    timezone = tf.timezone_at(lng=longitude, lat=latitude)
    avg_five_years = get_avg_five_years(longitude, latitude, today, timezone)
    temp_today = get_temp_today(longitude, latitude, today, timezone)
    today_pct = int(round(temp_today / avg_five_years, 2) * 100)
    if today_pct > 100:
        today_pct -= 100
        above_below = "above"
    else:
        today_pct = 100 - today_pct
        above_below = "below"
    return {
        "temp_today": temp_today,
        "avg_five_years": avg_five_years,
        "today_pct": today_pct
    }
    # return f'Today is {today_pct}% {above_below} the average temperature over the past five years.'


if __name__ == "__main__":
    # print(main_function())
    print("Running from command line, probably.")
    print("Using test postcode EH1 2NG")
    print(main_function("EH12NG"))
