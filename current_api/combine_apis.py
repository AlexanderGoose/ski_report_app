import json

# open all_resort_weather_data
with open('json_files/all_resort_weather_data.json', 'r') as file:
    all_data = json.load(file)

# open scraped_data
with open('json_files/scraped_data.json', 'r') as file:
    snow_data = json.load(file)

# start updating
resorts_lst = ['Arapahoe Basin', 'Copper Mountain', 'Steamboat', 'Winter Park']

for i in resorts_lst:
    all_data['i']
    pass

# update all data with new snow data
print(snow_data)
