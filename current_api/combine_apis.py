import json

# open all_resort_weather_data
with open('json_files/all_resort_weather_data.json', 'r') as file:
    all_data = json.load(file)

# open scraped_data
with open('json_files/scraped_data.json', 'r') as file:
    snow_data = json.load(file)

# start updating
resorts_lst = ['Arapahoe Basin', 'Copper', 'Steamboat', 'Winter Park']

for resort in resorts_lst:
    cur_res_snow_data = snow_data.get(resort)
    all_data[resort]['today']['snow'].update(cur_res_snow_data)
    
with open('json_files/all_resort_weather_data.json', 'w') as file:
    json.dump(all_data, file, indent=4)
