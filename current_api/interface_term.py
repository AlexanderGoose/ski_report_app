import json
import os
import time

# loads in normalized scores
file_path = '/Users/goose/Desktop/ski_report_app/current_api/normalized_resort_scores.json'
with open(file_path, 'r') as file:
    scores = json.load(file)

# loads in weather data
weather_file_path = '/Users/goose/Desktop/ski_report_app/current_api/all_resort_weather_data.json'
with open(weather_file_path, 'r') as file:
    weather = json.load(file)

# updated list without aspen mountains (they ain't included in the base pass)
resorts_lst = ['Arapahoe Basin', 'Copper Mountain', 'Eldora', 'Steamboat', 'Winter Park']

# grabs max resort, top three, and worst
top_resort = max(scores, key=scores.get)
top_three = list(scores.keys())[:3] # convert to list in order to index
worst = min(scores, key=scores.get)

# set conndition for while loop, other functions can break out of it by setting this to false
# TODO: allow a function to set this to false
done = True 

def clear_screen():
    os.system('clear')


# TODO: add in analysis which allows a user to look into the weather data
# will allow the user to compare multiple resorts to one another
def analysis():
    clear_screen()
    print("What would you like to analyze?")
    print("1 to compare")
    print("2 to check a resort")
    choice = input(">> ")
    
    def choose_resort(order):
        """allows user to inpu the res of their choice, repeats if not valid."""
        selection = input(f"Enter {order} resort >> ")
        selection = int(selection)
        valid_inputs = [1,2,3,4,5]
        if selection not in valid_inputs:
            print("invalide input")
            time.sleep(2)
            choose_resort()
        return selection
    
    if choice == "1":
        clear_screen()
        print("1 A Basin\n2 Copper\n3 Eldora\n4 Steamboat\n5 Winter Park")
        first_selection = choose_resort(order="first")
        second_selection = choose_resort(order="second")
    elif choice == "2":
        pass
    else:
        print("invalid input")
        time.sleep(2)
        analysis()

    def check_weather(resort1, resort2):
        # area to store explenations of weather
        return_statements = []
        # TODO: calculate snow
        # ex: if res_1["snow..."] -> print("{res 1} has more snow with {amount} in the past {timeframe}")
        snow_1_today = weather[resort1]["today"]["snow"]["snow_total"]
        snow_1_3     = weather[resort1]["three_day"]["snow"]["snow_total"]
        snow_1_7     = weather[resort1]["seven_day"]["snow"]["snow_total"]

        snow_2_today = weather[resort2]["today"]["snow"]["snow_total"]
        snow_2_3     = weather[resort2]["three_day"]["snow"]["snow_total"]
        snow_2_7     = weather[resort2]["seven_day"]["snow"]["snow_total"]

        if snow_1_today > snow_2_today:
            return_statements.append(f"{resort1} has more snow today.")
        else:
            return_statements.append(f"{resort2} has more snow today.")

        if snow_1_3 > snow_2_3:
            return_statements.append(f"{resort1} has had more snow in the last 3 days.")
        else:
            return_statements.append(f"{resort2} has had more snow in the last 3 days.")

        if snow_1_7 > snow_2_7:
            return_statements.append(f"{resort1} has had more snow in the last 7 days.")
        else:
            return_statements.append(f"{resort1} has had more snow in the last 7 days.")


        # TODO: compare winds and gusts

        # TODO: compare visibility

        # TODO: compare temperatures

        pass



def cont():
    choice = input("Continue? (Y/N): ")
    if choice == "Y" or choice == 'y':
        return True
    elif choice == "N" or choice == 'n':
        print("exiting...")
        return False
    else:
        # invalid input
        print("Invalid input! Enter 'Y' or 'N'!")
        time.sleep(2)
        clear_screen()
        cont()

def interface(score_dict):
    done = False
    while not done:
        clear_screen()
        print("\nWelcome to the Ikon selector!")
        print("Type 1 for top resort")
        print("Type 3 for top 3 resorts")
        print("Type 0 for worst resort")
        print("Type 5 for all")
        print("Type 7 for analysis\n")

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
                # prints all scores, * 100 to make more readable
                print("\n".join(f"{resort}: {int(score * 100)}" for resort, score in scores.items()))
            elif first_selection == 7:
                analysis()
            else:
                print("Invalid input.")
                time.sleep(2)
                continue # this goes back to the top of try :)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

        # if cont returns T, done stays F
        # if cont returns F, then done goes to T
        done = not cont()
            

clear_screen()
interface(scores)