import json



# open all_resort_weather_data
with open('json_files/all_resort_weather_data.json', 'r') as file:
    all_data = json.load(file)

# open scraped_data
with open('json_files/scraped_data.json', 'r') as file:
    snow_data = json.load(file)

# open lift reports
with open('json_files/lift_reports.json', 'r') as file:
    lift_data = json.load(file)



# start updating
resorts_lst = ['Arapahoe Basin', 'Copper', 'Steamboat', 'Winter Park']
liftie_resorts_lst = ['abasin', 'copper', 'steamboat', 'winter-park']

curr_index = 0
for resort in resorts_lst:
    cur_res_snow_data = snow_data.get(resort)
    all_data[resort]['today']['snow'].update(cur_res_snow_data)

    # # handle different naming conventions used in liftie api
    # liftie_res = liftie_resorts_lst[curr_index] # grabs liftie name
    # needed_lift_data = lift_data[liftie_res]

    # # ensure lifts still exists
    # if "lifts" not in all_data[resort]['today']:
    #     all_data[resort]['today']['lifts'] = ''
    
    # all_data[resort]['today']['lifts'].update(needed_lift_data)

    curr_index += 1
    
with open('json_files/all_resort_weather_data.json', 'w') as file:
    json.dump(all_data, file, indent=4)
