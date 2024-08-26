import requests
import time
import json


def breckenridge_get():

    breck_data = {
        'Mountain': '',
        'previous_weather': {},
        'today': {}
    }

    # info for crafting historical link
    API_KEY = open('api-key.txt', 'r').read().strip()
    BASE_URL_HIS = 'https://history.openweathermap.org/data/2.5/history/city?lat='

    # coordinates
    LAT = '39.480227'  
    LON = '-106.066698' 

    # goes back 7 days
    start = str(int(time.time()) - 7 * 86400)
    end = str(int(time.time()))

    url_historical = BASE_URL_HIS + LAT + '&lon=' + LON + '&type=hour&start=' + start + '&end=' + end + '&appid=' + API_KEY

    r_his = requests.get(url_historical)

    # first call - gets historical data
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

        breck_data['previous_weather']['snow_7_days'] = round(sum(total_snow_7_days),1)
        breck_data['previous_weather']['snow_2_days'] = round(sum(total_snow_48_hours), 1)
        breck_data['previous_weather']['snow_24_hours'] = round(sum(total_snow_48_hours[24:]), 1)
    
    else:
        print(f"Failed to retrieve data: {r_his.status_code}")
        

    ###################################### 
        
    def kelvin_to_far(kelvin):
        celsius = kelvin - 273.15
        farenheit = celsius * (9/5)
        farenheit = farenheit + 32
        return farenheit

    ###################################### 

    url_daily = "https://api.openweathermap.org/data/2.5/forecast/daily?lat=" + LAT + "&lon=" + LON +"&cnt=1" + "&appid=" + API_KEY

    # Make the API request
    response = requests.get(url_daily)

    if response.status_code == 200:
        data = response.json()
        formatted_data = json.dumps(data, indent=4) # formats into a json with proper indentation
        # print(formatted_data)

        # Get min and max temperatures for today
        breck_data['Mountain'] = data['city']['name']
        breck_data['today']['min'] = round(kelvin_to_far(data['list'][0]['temp']['min']), 1)
        breck_data['today']['max'] = round(kelvin_to_far(data['list'][0]['temp']['max']), 1)
        breck_data['today']['wind'] = round((data['list'][0]['speed']) * 2.237, 1)
        breck_data['today']['gust'] = round((data['list'][0]['gust']) * 2.237, 1)

        formatted_data = json.dumps(breck_data, indent=4) # formats into a json with proper indentation
        print(formatted_data)

    return breck_data

breckenridge_get()


# add this new breck_data JSON to a postgreSQL server
# be able to querry based on mountain, pull the data,
# and use it to make a ranking.
# Determine the math to be done to create the rankings.