"""

Here we decide what is good or bad weather
This needs a lot of work. It is currrently very subjective.

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
        print(key)
        curr_res_score = 0

        # Today's snow -- this may be using the wrong input? As in from midnight to now, instead of today's total predicted amount

        # Scoring logic for 24-hour snowfall
        # Scoring logic for 24-hour snowfall
        if int(weather_dict[key]["today"]["snow"]["24hr_snow"]) > 8:
            curr_res_score += 6  # High score for significant snowfall in the last 24 hours
        elif 8 >= int(weather_dict[key]["today"]["snow"]["24hr_snow"]) > 4:
            curr_res_score += 4  # Moderate snowfall
        elif 4 >= int(weather_dict[key]["today"]["snow"]["24hr_snow"]) > 0:
            curr_res_score += 2  # Light snowfall

        # Scoring logic for 48-hour snowfall
        if int(weather_dict[key]["today"]["snow"]["48hr_snow"]) > 12:
            curr_res_score += 5  # High score for significant snowfall over the last 48 hours
        elif 12 >= int(weather_dict[key]["today"]["snow"]["48hr_snow"]) > 6:
            curr_res_score += 3  # Moderate snowfall
        elif 6 >= int(weather_dict[key]["today"]["snow"]["48hr_snow"]) > 0:
            curr_res_score += 1  # Light snowfall

        # Scoring logic for base snow depth
        if int(weather_dict[key]["today"]["snow"]["base_snow"]) > 60:
            curr_res_score += 5  # High score for deep base snow
        elif 60 >= int(weather_dict[key]["today"]["snow"]["base_snow"]) > 30:
            curr_res_score += 3  # Moderate base snow
        elif 30 >= int(weather_dict[key]["today"]["snow"]["base_snow"]) > 0:
            curr_res_score += 1  # Light base snow

        # Temperature
        if 35 >= weather_dict[key]["today"]["temps"]["avg_temp"] >= 20 and weather_dict[key]["today"]["temps"]["max_temp"] <= 40:
            curr_res_score += 6
        elif 30 >= weather_dict[key]["today"]["temps"]["avg_temp"] >= 15:
            curr_res_score += 4
        elif weather_dict[key]["today"]["temps"]["max_temp"] >= 45:  # too hot
            curr_res_score -= 2
        elif weather_dict[key]["today"]["temps"]["avg_temp"] <= 5:  # too cold
            curr_res_score -= 2

        # Wind 
        if weather_dict[key]["today"]["wind"]["avg_wind"] < 5:
            curr_res_score += 5
        elif 10 >= weather_dict[key]["today"]["wind"]["avg_wind"] >= 5:
            curr_res_score += 3
        elif 20 >= weather_dict[key]["today"]["wind"]["avg_wind"] > 10:
            curr_res_score += 1
        elif weather_dict[key]["today"]["wind"]["avg_wind"] > 20:
            curr_res_score -= 3

        # Gusts (because they suck)
        if weather_dict[key]["today"]["wind"]["max_gusts"] <= 15:
            curr_res_score += 3
        # the range in between is fine so no points there
        elif weather_dict[key]["today"]["wind"]["max_gusts"] > 25:
            curr_res_score -= 3

        # Visibility (is this adding too many points??)
        if weather_dict[key]["today"]["vis"]["avg_vis"] >= 9000:
            curr_res_score += 6
        elif 9000 > weather_dict[key]["today"]["vis"]["avg_vis"] >= 7500:
            curr_res_score += 4
        elif 7500 > weather_dict[key]["today"]["vis"]["avg_vis"] >= 5000:
            curr_res_score += 2
        elif 5000 > weather_dict[key]["today"]["vis"]["avg_vis"] >= 3000:
            curr_res_score += 1

        resort_scores[key] = curr_res_score

    # TEMPERORY
    # formatting the data to print better in the terminal for debugging
    # sorts by the score from highest to lowest
    sorted_resort_scores = dict(sorted(resort_scores.items(), key=lambda item: item[1], reverse=True))
    # join items into a single string with newlines in between resorts

    # return formatted_output
    return sorted_resort_scores


# testing
# 1 - read in json file w/ full path
# 2 - call and print above function
weather_data = read_json_file('/Users/goose/Desktop/ski_report_app/current_api/json_files/all_resort_weather_data.json')
# print(count_score(weather_data))

scores = count_score(weather_data)
formatted_output = "\n".join(f"{resort}: {value}" for resort, value in scores.items())
print("Initial Scores:\n")
print(formatted_output)
print('\n')

# TODO: begin normalizing the data
max_score = max(scores.values())
min_score = min(scores.values())

normalized_scores = {}
for resort, value in scores.items():
    norm_score = (value - min_score) / (max_score - min_score)
    normalized_scores[resort] = round(norm_score, 2)

formatted__normal_output = "\n".join(f"{resort}: {value}" for resort, value in normalized_scores.items())
print('Normalized Scores:\n')
print(formatted__normal_output)

# save normalized data as JSON
with open("json_files/normalized_resort_scores.json", "w") as file:
    json.dump(normalized_scores, file, indent=4)




