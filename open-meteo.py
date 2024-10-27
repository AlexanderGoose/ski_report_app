import openmeteo_requests
import requests_cache
import pandas as pd 
from retry_requests import retry
from ikon import resorts, resorts_lst
from datetime import datetime
import json

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"

def cel_to_far(cel_temp):
    farenheit = cel_temp * (9/5)
    farenheit = farenheit + 32
    return farenheit

def get_weather_():

    # initializing dictionary to hold weather data
    weather_data = {}
    # for resort_name in resorts_lst:
    #     resort_info = resorts.get(resort_name)

    #     # ensure it's in the list
    #     if resort_info:
    #         # first, grab coordinates
    #         curr_lon = str(resort_info['LON'])
    #         curr_lat = str(resort_info['LAT'])

        # use above data to pass to API
    params = {
        # 'latitude': curr_lat,
        # 'longitude': curr_lon,
        "latitude": 39.4817,
        "longitude": -106.0383,
        "hourly": ["temperature_2m", "apparent_temperature", "rain", "visibility", "wind_speed_10m", "wind_gusts_10m"],
        "past_days": 7,
        "forecast_days": 1
    }

    responses = openmeteo.weather_api(url, params=params)

    # create JSON template for weather_data dictionary using nested dicts
    # weather_data[resort_name] = {'today': {}, 'prev_weather': {}, }

    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_rain = hourly.Variables(2).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(5).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["rain"] = hourly_rain
    hourly_data["visibility"] = hourly_visibility
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    # print(hourly_dataframe)
    return hourly_dataframe

hr_df = get_weather_()

# get data for today: high and low temps, vis, wind speed, and gusts

class todays_weather():
    
    def __init__(self, df):
        self.df = df

    def get_todays_temp(self):
        todays_temp_data = {
            'min_temp': round(cel_to_far(min(self.df['temperature_2m'])),2),
            'max_temp': round(cel_to_far(max(self.df['temperature_2m'])),2),
            'avg_temp': round(float(cel_to_far(self.df['temperature_2m'].mean())),2)
        }
        return todays_temp_data

    def visibility(self):
        vis_data = {
            'min_vis': round(min(self.df['visibility']),2),
            'max_vis': round(max(self.df['visibility']),2),
            'avg_vis': round(float(self.df['visibility'].mean()),)
        }
        print(vis_data)
        return vis_data
    
    def rain(self):
        rain_data = {
            'total_rain': sum(self.df['rain'])
        }
        print(rain_data)
        return rain_data
    
    def wind(self):
        wind_data = {
            'avg_wind': float(self.df['wind_speed_10m'].mean()),
            'max_gusts': max(self.df['wind_gusts_10m']),
            'avg_gusts': float(self.df['wind_gusts_10m'].mean())
        }
        print(wind_data)
        return wind_data

# example = todays_weather(hr_df)


def todays_range(df):
    # Get today's date in the format 'YYYY-MM-DD'
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # Filter rows where only the date part matches today's date
    today_data = df[df['date'].dt.strftime('%Y-%m-%d') == today_date]
    
    return today_data


def weather_range_json(df):
    weather_data = {}
    range_data = todays_weather(df)

    weather_data['temps'] = range_data.get_todays_temp()
    weather_data['vis'] = range_data.visibility()
    weather_data['rain'] = range_data.rain()
    weather_data['wind'] = range_data.wind()

    formatted_data = json.dumps(weather_data, indent=4)
    return formatted_data

print(weather_range_json(hr_df))

def three_day_range():
    pass
def seven_day_range():
    pass




# divy up the days into their own thing

# for each time frame (7 day, 3 day, today)
# find total snow (rain)