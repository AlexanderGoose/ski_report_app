import openmeteo_requests
import requests_cache
import pandas as pd 
from retry_requests import retry
from ikon import resorts, resorts_lst
from datetime import datetime, timedelta
import json


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"

# API returns temps as C, need to ALWAYS convert to F
def cel_to_far(cel_temp):
    farenheit = cel_temp * (9/5)
    farenheit = farenheit + 32
    return farenheit

# TODO: remove unecessary data pulls such as temperature, wind, vis for last week,
# we want to only have 7 and 3 day data for snowfall, all others should be daily weather variables

def get_weather_():
    """
    makes the api call, adds all info to dictionary, then converts to dataframe
    RETURNS df
    """

    # add each individual resort here, after loop combine all into one df
    all_resorts_data = []

    for resort_name in resorts_lst:
        resort_info = resorts.get(resort_name)


        # first, grab coordinates
        curr_lon = str(resort_info['LON'])
        curr_lat = str(resort_info['LAT'])

    
        params = {
            'latitude': curr_lat,
            'longitude': curr_lon,
            "hourly": ["temperature_2m", "apparent_temperature", "snowfall", "visibility", "wind_speed_10m", "wind_gusts_10m", "cloud_cover"],
            "current": "cloud_cover",
            # "daily": "snowfall_sum",
            "past_days": 7,
            "forecast_days": 1,
            "timezone": "America/Denver"
        }

        # print(f'CURR RES: {resort_name}')
        responses = openmeteo.weather_api(url, params=params)

        response = responses[0]

        # Process hourly data. The order of variables needs to be the same as requested.
        # TODO: add in daily snow
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()         # temperature
        hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()   # feels like?
        hourly_snow = hourly.Variables(2).ValuesAsNumpy()                   # snow
        hourly_visibility = hourly.Variables(3).ValuesAsNumpy()             # visibility
        hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()         # wind speed
        hourly_wind_gusts_10m = hourly.Variables(5).ValuesAsNumpy()         # wind gust
        # TODO: Find out why cloud cover returns such strange values
        #hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()   
        #print(hourly_cloud_cover)   

        # creates dictionary, first adds data using datetime as only column
        # this dictionary is for only ONE resort, the current one in the loop
        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        # adds to dictionary created above
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["apparent_temperature"] = hourly_apparent_temperature
        hourly_data["snow"] = hourly_snow
        hourly_data["visibility"] = hourly_visibility
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

        # Convert dictionary to DataFrame (important for concatination later)
        hourly_data = pd.DataFrame(data=hourly_data)
        hourly_data['resort'] = resort_name  # Add resort name as a column for reference!!

        # Append to the list of all resorts' data
        all_resorts_data.append(hourly_data)

    # Combine all resort data into a single DataFrame
    combined_df = pd.concat(all_resorts_data, ignore_index=True)
    return combined_df

# create a df by calling above function
hr_df = get_weather_()
# print(hr_df)


# TODO: rename class to something more generic and refactor where its called
class todays_weather():
    """
    gets various weather data from a dataframe.\n
    temperature, vis, and wind only include data during operational hours to avoid night data skewing metrics.\n
    snow/rain data included for all 24 hours of day.\n
    RETURNS dictionaries of values
    """
    def __init__(self, df):
        self.df = df

    def get_todays_temp(self):
        # Filter for hours between 8 AM and 4 PM
        daytime_df = self.df[(self.df['date'].dt.hour >= 8) & (self.df['date'].dt.hour <= 16)]
        
        # Calculate min, max, and avg temperature for filtered hours
        todays_temp_data = {
            'min_temp': round(float(cel_to_far(daytime_df['temperature_2m'].min())), 2),
            'max_temp': round(float(cel_to_far(daytime_df['temperature_2m'].max())), 2),
            'avg_temp': round(float(cel_to_far(daytime_df['temperature_2m'].mean())), 2)
        }
        # print(todays_temp_data)
        return todays_temp_data

    def visibility(self):
        # Filter the data for times between 8 AM and 4 PM
        filtered_df = self.df[(self.df['date'].dt.hour >= 8) & (self.df['date'].dt.hour <= 16)]
        
        # Calculate min, max, and avg visibility for the filtered hours
        vis_data = {
            'min_vis': int(float(filtered_df['visibility'].min()) / 3.28),
            'max_vis': int(float(filtered_df['visibility'].max()) / 3.28),
            'avg_vis': int(float(filtered_df['visibility'].mean()) / 3.28)
        }
        # print(vis_data)
        return vis_data
    
    def snow(self):
        # for now, just make them empty and update with scraped data
        snow_data = {
            # 'total_snow': round(sum(self.df['snow']),2)
            '24hr_snow': '',
            '48hr_snow': '',
            'base_snow': ''
        }
        # print(rain_data)
        return snow_data
    
    def wind(self):
        filtered_df = self.df[(self.df['date'].dt.hour >= 8) & (self.df['date'].dt.hour <= 16)]
        wind_data = {
            'avg_wind': int(float(filtered_df['wind_speed_10m'].mean())),
            'max_gusts': int(max(filtered_df['wind_gusts_10m'])),
            'avg_gusts': int(float(filtered_df['wind_gusts_10m'].mean()))
        }
        return wind_data


"""
these 3 functions create dfs of specific time ranges\n
RETURNS dfs
"""
def todays_range(df):
    # Get today's date in the format 'YYYY-MM-DD'
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # Filter rows where only the date part matches today's date
    today_data = df[df['date'].dt.strftime('%Y-%m-%d') == today_date]
    
    return today_data

def three_day_range(df):
    last_3_days = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(3)]
    three_day_data = df[df['date'].dt.strftime('%Y-%m-%d').isin(last_3_days)]
    return three_day_data

def seven_day_range(df):
    last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    seven_day_data = df[df['date'].dt.strftime('%Y-%m-%d').isin(last_7_days)] 
    return seven_day_data


# create 3 new dfs by calling above functions
today = todays_range(hr_df)
three_day = three_day_range(hr_df)
seven_day = seven_day_range(hr_df)


def weather_dict_maker(df):
    """
    using a df, this creates a dictionary of various weather information\n
    uses todays_weather to generate nested dictionaris\n
    RETURNS dictionary
    """
    weather_dict = {}

    range_data = todays_weather(df)


    weather_dict['temps'] = range_data.get_todays_temp()
    weather_dict['vis'] = range_data.visibility()
    weather_dict['snow'] = range_data.snow()
    weather_dict['wind'] = range_data.wind()
    return weather_dict


def weather_json_maker(today_df, three_day_df, seven_day_df):
    """
    creates weather_data which contains 1, 3, and 7 day data as dictionaries\n
    combines 3 dictionaries into one and converts it to a JSON\n
    TODO: rename function as it no longer returns a JSON (this was an issue for the below loop, needed them to be dicts)
    RETURNS dictionary
    """
    today_dict = weather_dict_maker(today_df)
    three_day_dict = weather_dict_maker(three_day_df)
    seven_day_dict = weather_dict_maker(seven_day_df)

    weather_data = {
        'today': today_dict,
        'three_day': three_day_dict,
        'seven_day': seven_day_dict
    }
    return weather_data


all_resort_data_dict = {}
for resort_name in resorts_lst:
    # print(resort_name)
    curr_resort = hr_df[hr_df['resort'] == resort_name]
    curr_today = today[today['resort'] == resort_name]
    curr_three_day = three_day[three_day['resort'] == resort_name]
    curr_seven_day = seven_day[seven_day['resort'] == resort_name]
    
    curr_weather_data = weather_json_maker(curr_today, curr_three_day, curr_seven_day)
    all_resort_data_dict[resort_name] = curr_weather_data

# write all data to a JSON file. We will pull data from the JSON later.
with open("json_files/all_resort_weather_data.json", "w") as file:
    json.dump(all_resort_data_dict, file, indent = 4)
