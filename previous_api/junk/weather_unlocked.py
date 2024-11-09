import requests
import pandas as pd

def get_weather_unlocked_data():
    app_id="f0815050"
    app_key="fab11f71db8f972d6c021d93addf20b9"
    resort_id = 303001
    url = f"https://api.weatherunlocked.com/api/resortforecast/{resort_id}?app_id={app_id}&app_key={app_key}"
    
    r = requests.get(url)
    if r.status_code == 200:
        print(r.headers['content-type']) # tells us if it's a JSON
        print(r.text)
        print(r.json()) # prints it as a JSON   
    else:
        print(f"Error retrieving data. Status code: {r.status_code}")
