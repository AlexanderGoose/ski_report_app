import json
import os

# TODO: make the option to use ALL CO resorts and can filter down options in here? 
# however, the perk of using so few means the API call is very fast!

file_path = '/Users/goose/Desktop/ski_report_app/current_api/normalized_resort_scores.json'
with open(file_path, 'r') as file:
    scores = json.load(file)

weather_file_path = '/Users/goose/Desktop/ski_report_app/current_api/all_resort_weather_data.json'
with open(weather_file_path, 'r') as file:
    weather = json.load(file)

resorts_lst = ['Arapahoe Basin', 'Aspen Highlands', 'Aspen Mountain',
            'Buttermilk (Aspen)', 'Copper Mountain', 'Eldora',
            'Snowmass (Aspen)', 'Steamboat', 'Winter Park']

# max_key = max(data, key=data.get)
top_resort = max(scores, key=scores.get)
top_three = list(scores.keys())[:3]

worst = min(scores, key=scores.get)

done = True 

# TODO: add in analysis which allows a user to look into the weather data
# will allow the user to compare multiple resorts to one another
def analysis():
    pass

def interface(score_dict):
    print("\nWelcome to the Ikon selector!")
    print("Type 1 for top resort")
    print("Type 3 for top 3 resorts")
    print("Type 0 for worst resort")
    print("Type 5 for all\n")
    print("Type 7 for analysis")

    first_selection = input(">> ")
    try:
        first_selection = int(first_selection)
        if first_selection == 1:
            print(top_resort)
        elif first_selection == 3:
            print("\n".join(resort for resort in top_three))
        elif first_selection == 0:
            print(worst)
        elif first_selection == 5:
            
            print("\n".join(f"{resort}: {int(score * 100)}" for resort, score in scores.items()))
    except:
        print("Invalid input.")

while done:
    interface(scores)