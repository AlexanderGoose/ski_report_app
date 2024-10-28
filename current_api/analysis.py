"""

Here we decide what is good or bad weather

------------------------------------ snow
Snowfall:

last 7 days ->
    - 12+ inches    -> 5 points
    - 6 - 12 inches -> 3 points
    - 1 - 6 inches  -> 1 point

last 3 days ->
    - 12+ inches    -> 5 points
    - 6 - 12 inches -> 3 points
    - 1 - 6 inches  -> 1 point

    
------------------------------------ temp
Temperature:
if avg_temp >= 20 and avg_temp <= 40 and max_temp <= 40 -> 5 points (most ideal)
elif avg_temp >= 10 and avg_temp <= 30 -> 3 points 
elif max_temp >= 50 -> -1 point (too hot)
elif avg_temp < 10 -> -1 point (too cold)


------------------------------------ wind
Wind Speed:
if avg_wind < 0 -> 5 points
elif avg_wind > 5 and avg_wind <= 15 -> 3 points
elif avg_wind > 15 and avg-wind <= 20 -> 0 points
elif avg_wind > 20 -> -1 point

------------------------------------ gusts
Gusts:
if max_gusts <= 15 -> 3 points
elif max_gusts >= 15 and max_gusts <= 30 -> 0 point ???
elif max_gusts >= 30 -> -1 points


------------------------------------ vis
Visibility:

if avg_vis == 9000 -> 5 points
elif avg_vis >= 7000 and avg_vis < 9000 -> 4 points
elif avg_vis >= 4500 and avg_vis < 7000 -> 2 points
else -> 0 points

"""

import json
import os

def read_json_file(file_path):
    file_path = os.path.expanduser(file_path)

    with open(file_path, 'r') as file:
        weather_data = json.load(file)
    
    return weather_data # returns as dict 

def count_score(weather_dict):
    resort_scores = {}
    for key, values in weather_dict.items():
        curr_res_score = 0

        # 7 day snow
        if weather_dict[key]["seven_day"]["rain"]["total_rain"] > 12:
            curr_res_score += 5
        elif 12 >= weather_dict[key]["seven_day"]["rain"]["total_rain"] > 6:
            curr_res_score += 3
        elif 6 >= weather_dict[key]["seven_day"]["rain"]["total_rain"] > 0:
            curr_res_score += 1

        # 3 day snow
        if weather_dict[key]["three_day"]["rain"]["total_rain"] > 12:
            curr_res_score += 5
        elif 12 >= weather_dict[key]["three_day"]["rain"]["total_rain"] > 6:
            curr_res_score += 3
        elif 6 >= weather_dict[key]["three_day"]["rain"]["total_rain"] > 0:
            curr_res_score += 1

        # temps
        if 40 >= weather_dict[key]["today"]["temps"]["avg_temp"] >= 20 and weather_dict[key]["today"]["temps"]["max_temp"] <= 40:
            curr_res_score += 5
        elif 30 >= weather_dict[key]["today"]["temps"]["avg_temp"] >= 10:
            curr_res_score += 3
        elif weather_dict[key]["today"]["temps"]["max_temp"] >= 50: # too hot
            curr_res_score -= 1
        elif weather_dict[key]["today"]["temps"]["avg_temp"] >= 10: # too cold
            curr_res_score -= 1

        # wind
        if weather_dict[key]["today"]["wind"]["avg_wind"] < 5:
            curr_res_score += 5
        elif 15 >= weather_dict[key]["today"]["wind"]["avg_wind"] >= 5:
            curr_res_score += 3
        elif weather_dict[key]["today"]["wind"]["avg_wind"] >= 20:
            curr_res_score -= 1

        # gusts
        if weather_dict[key]["today"]["wind"]["max_gusts"] <= 15:
            curr_res_score += 2
        elif weather_dict[key]["today"]["wind"]["max_gusts"] >= 20:
            curr_res_score -= 1
        elif 15 >= weather_dict[key]["today"]["wind"]["avg_gusts"] >= 0:
            curr_res_score += 2
        elif weather_dict[key]["today"]["wind"]["avg_gusts"] >= 25: # too windy
            curr_res_score -= 3

        # vis
        if weather_dict[key]["today"]["vis"]["avg_vis"] >= 8500:
            curr_res_score += 5
        elif 8500 > weather_dict[key]["today"]["vis"]["avg_vis"] >= 7000:
            curr_res_score += 4
        elif 7000 > weather_dict[key]["today"]["vis"]["avg_vis"] >= 4500:
            curr_res_score += 2

        resort_scores[key] = curr_res_score

    sorted_resort_scores = dict(sorted(resort_scores.items(), key=lambda item: item[1], reverse=True))
    # Join items into a single string with newlines
    formatted_output = "\n".join(f"{resort}: {value}" for resort, value in sorted_resort_scores.items())

    return formatted_output




        


weather_data = read_json_file('/Users/goose/Desktop/ski_report_app/current_api/all_resort_weather_data.json')
print(count_score(weather_data))


