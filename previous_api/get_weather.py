import requests
import time
import json
from resort_data import resorts, resorts_lst

def kelvin_to_far(kelvin):
    celsius = kelvin - 273.15
    farenheit = celsius * (9/5)
    farenheit = farenheit + 32
    return farenheit

def get_weather():
    weather_data = {}
    API_KEY = open('api-key.txt', 'r').read().strip()

    for resort_name in resorts_lst:
        resort_info = resorts.get(resort_name)

        if resort_info:
            curr_lon = str(resort_info['LON'])
            curr_lat = str(resort_info['LAT'])
            weather_data[resort_name] = {'today': {},'previous_weather': {}, }

            # info for crafting historical link
            
            BASE_URL_HIS = 'https://history.openweathermap.org/data/2.5/history/city?lat='
            
            # goes back 7 days
            start = str(int(time.time()) - 7 * 86400)
            end = str(int(time.time()))

            # dynamically created URLs
            url_historical = BASE_URL_HIS + curr_lat + '&lon=' + curr_lon + '&type=hour&start=' + start + '&end=' + end + '&appid=' + API_KEY
            url_daily = "https://api.openweathermap.org/data/2.5/forecast/daily?lat=" + curr_lat + "&lon=" + curr_lon + "&cnt=1" + "&appid=" + API_KEY
            #url_daily = f"https://api.openweathermap.org/data/2.5/onecall?lat={curr_lat}&lon={curr_lon}&exclude=hourly,minutely&appid={API_KEY}"
            # r_his = requests.get(url_historical)

            # Make the API request FOR CURRENT WEATHER
            try:
                response = requests.get(url_daily)
                response.raise_for_status()  # Raises an error for bad status codes
            except requests.exceptions.RequestException as e:
                print(f"Error with resort {resort_name}: {e}")
                continue

            if response.status_code == 200:
                data = response.json()

                # Get min and max temperatures for today
                weather_data[resort_name]['today']['min'] = round(kelvin_to_far(data['list'][0]['temp']['min']), 1)
                weather_data[resort_name]['today']['max'] = round(kelvin_to_far(data['list'][0]['temp']['max']), 1)
                weather_data[resort_name]['today']['wind'] = round((data['list'][0]['speed']) * 2.237, 1)
                weather_data[resort_name]['today']['gust'] = round((data['list'][0]['gust']) * 2.237, 1)
            
            else:
                print(f"Failed to retrieve data: {response.status_code}")


            # Make the API request FOR HISTORICAL WEATHER
            try:
                r_his = requests.get(url_historical)
                r_his.raise_for_status()  # Raises an error for bad status codes
            except requests.exceptions.RequestException as e:
                print(f"Error with resort {resort_name}: {e}")
                continue

            # gets historical data
            if r_his.status_code == 200:
                data = r_his.json()
                # print(data)
                total_snow_7_days = []
                total_snow_48_hours = []
                for entry in data.get('list', []):
                    # Snowfall in the last 1 hour, in mm
                    snowfall = entry.get('rain', {}).get('1h', 0) 
                    total_snow_7_days.append(snowfall)
                
                past_48_hours = total_snow_7_days[120:]
                for entry in past_48_hours: 
                    total_snow_48_hours.append(entry)

                weather_data[resort_name]['previous_weather']['snow_7_days'] = round(sum(total_snow_7_days),1)
                weather_data[resort_name]['previous_weather']['snow_2_days'] = round(sum(total_snow_48_hours), 1)
                weather_data[resort_name]['previous_weather']['snow_24_hours'] = round(sum(total_snow_48_hours[24:]), 1)
    return weather_data

data = get_weather()
formatted_data = json.dumps(data, indent=4) # formats into a json with proper indentation
print(formatted_data)