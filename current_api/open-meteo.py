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

def get_weather_():
    """
    makes the api call, adds all info to dictionary, then converts to dataframe
    RETURNS df
    """

    # add each individual resort here, after loop combine all into one df
    all_resorts_data = []

    for resort_name in resorts_lst:
        resort_info = resorts.get(resort_name)

        # ensure it's in the list
        if resort_info:
            # first, grab coordinates
            curr_lon = str(resort_info['LON'])
            curr_lat = str(resort_info['LAT'])

        
            params = {
                'latitude': curr_lat,
                'longitude': curr_lon,
                # "latitude": 39.4817,
                # "longitude": -106.0383,
                "hourly": ["temperature_2m", "apparent_temperature", "rain", "visibility", "wind_speed_10m", "wind_gusts_10m"],
                "past_days": 7,
                "forecast_days": 1
            }

            # print(f'CURR RES: {resort_name}')
            responses = openmeteo.weather_api(url, params=params)

            response = responses[0]

            # Process hourly data. The order of variables needs to be the same as requested.
            # TODO: add in snow when winter comes
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()         # temperature
            hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()   # feels like?
            hourly_rain = hourly.Variables(2).ValuesAsNumpy()                   # rain 
            hourly_visibility = hourly.Variables(3).ValuesAsNumpy()             # visibility
            hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()         # wind speed
            hourly_wind_gusts_10m = hourly.Variables(5).ValuesAsNumpy()         # wind gust

            # creates dictionary, first adds data using datetime as only column
            hourly_data = {"date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )}

            # adds to dictionary created above
            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["apparent_temperature"] = hourly_apparent_temperature
            hourly_data["rain"] = hourly_rain
            hourly_data["visibility"] = hourly_visibility
            hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
            hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

            # Convert dictionary to DataFrame
            hourly_data = pd.DataFrame(data=hourly_data)
            hourly_data['resort'] = resort_name  # Add resort name as a column for reference

            # Append to the list of all resorts' data
            all_resorts_data.append(hourly_data)

    # hourly_dataframe = pd.DataFrame(data = hourly_data)
    # Combine all resort data into a single DataFrame
    combined_df = pd.concat(all_resorts_data, ignore_index=True)
    return combined_df

# create a df by calling above function
hr_df = get_weather_()
print(hr_df)

# TODO: rename class to something more generic and refactor where its called
class todays_weather():
    """
    gets various weather data from a dataframe.\n
    RETURNS dictionaries of values
    """
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
        return vis_data
    
    def rain(self):
        rain_data = {
            'total_rain': round(sum(self.df['rain']),2)
        }
        return rain_data
    
    def wind(self):
        wind_data = {
            'avg_wind': round(float(self.df['wind_speed_10m'].mean()),2),
            'max_gusts': round(max(self.df['wind_gusts_10m']),2),
            'avg_gusts': round(float(self.df['wind_gusts_10m'].mean()),)
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
    weather_dict['rain'] = range_data.rain()
    weather_dict['wind'] = range_data.wind()
    return weather_dict


def weather_json_maker(today_df, three_day_df, seven_day_df):
    """
    creates weather_data which contains 1, 3, and 7 day data as dictionaries\n
    combines 3 dictionaries into one and converts it to a JSON\n
    RETURNS JSON
    """
    today_dict = weather_dict_maker(today_df)
    three_day_dict = weather_dict_maker(three_day_df)
    seven_day_dict = weather_dict_maker(seven_day_df)

    weather_data = {
        'today': today_dict,
        'three_day': three_day_dict,
        'seven_day': seven_day_dict
    }

    # formatted_data = json.dumps(weather_data, indent=4)
    # return formatted_data
    return weather_data

# used for testing above function
# print(weather_json_maker(today, three_day, seven_day))

all_resort_data_dict = {}
for resort_name in resorts_lst:
    # print(resort_name)
    curr_resort = hr_df[hr_df['resort'] == resort_name]
    curr_today = today[today['resort'] == resort_name]
    curr_three_day = three_day[three_day['resort'] == resort_name]
    curr_seven_day = seven_day[seven_day['resort'] == resort_name]
    
    curr_weather_data = weather_json_maker(curr_today, curr_three_day, curr_seven_day)
    all_resort_data_dict[resort_name] = curr_weather_data

# all_resort_data = json.dumps(all_resort_data_dict, indent = 4)
with open("all_resort_weather_data.json", "w") as file:
    json.dump(all_resort_data_dict, file, indent = 4)



# divy up the days into their own thing

# for each time frame (7 day, 3 day, today)
# find total snow (rain)
"""
I need to make the other functions simply work through a loop. Still want to split by time frames
and return the same information in the todays_weather() class, but like: 'resort': {todays_weather}
"""