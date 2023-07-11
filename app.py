from flask import Flask
from tempercent import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    longitude, latitude = longlat_from_postcode("EH51SG")
    today = date.today()
    timezone = "GMT"
    avg_five_years = get_avg_five_years(longitude, latitude, today, timezone)
    temp_today = get_temp_today(longitude, latitude, today, timezone)
    today_pct = int(round(temp_today / avg_five_years, 2) * 100)
    if today_pct > 100:
        today_pct -= 100
        above_below = "above"
    else:
        today_pct = 100 - today_pct
        above_below = "below"
    outstr = f'Today is {today_pct}% {above_below} the average temperature over the past five years.'
    return f"<h1>{outstr}</h1>"    
    
    
@app.route("/api")
def return_json():
    return "you tried"