import json
import os
import time


# TODO: try to limit how nested/deep selections have to go.
# for ex: cold eliminate all of 'check resort' with an overall from home screen
# then, isntead of analysis, remove that with the compare feature

# loads in normalized scores
file_path = '/Users/goose/Desktop/ski_report_app/current_api/json_files/normalized_resort_scores.json'
with open(file_path, 'r') as file:
    scores = json.load(file)

# loads in weather data
weather_file_path = '/Users/goose/Desktop/ski_report_app/current_api/json_files/all_resort_weather_data.json'
with open(weather_file_path, 'r') as file:
    weather = json.load(file)

# updated list without aspen mountains (they ain't included in the base pass)
resorts_lst = ['Arapahoe Basin', 'Copper', 'Steamboat', 'Winter Park']

# grabs max resort, top three, and worst
top_resort = max(scores, key=scores.get)
top_three = list(scores.keys())[:3] # convert to list in order to index
worst = min(scores, key=scores.get)



def clear_screen():
    os.system('clear')



def choose_resort():
    """   returns a number (1 - 4)   """
    q_list = ["Choose a resort:", "(1) A Basin", "(2) Copper", "(3) Steamboat", "(4) Winter Park"]
    choice = validate_user_input(q_list=q_list, valid_inputs_lst=[1,2,3,4])
    return choice



# TODO: create a function that validates user input instead of 
# doing this every time in the code. Checks for valid input and non empty, restarts if not 
def validate_user_input(q_list, valid_inputs_lst):
    """function prompts user to enter their input.\n
    Checks if non-empty and if considered valid for the context.\n
    Prints list of questions, takes input, returns choice as int."""
    clear_screen()
    valid = False
    while not valid:
        try:
            print("\n".join(q for q in q_list))
            user_input = input("\n>> ")
            if user_input: 
                if user_input == "q" or user_input == "quit": # gives the option to quit at any time
                    return "q"
                else:
                    user_input = int(user_input) # do this after to recognize empty string as input for testing
                    if user_input in valid_inputs_lst:
                        clear_screen()
                        return user_input
                    elif user_input not in valid_inputs_lst:
                        print(f"\nInvalid input. Valid inputs: {valid_inputs_lst} ")
                        time.sleep(2)
                        clear_screen()
            else:
                print("\nInput cannot be empty! Try again.")
                time.sleep(1)
                clear_screen()
        except Exception as e:
            print(f"Error: {e}")



def check_weather(resort1, resort2):

    """uses weather JSON to pull out data. Compares the data of two\n 
    resorts and makes assumptions based on comparisons."""

    # area to store explenations of weather
    return_statements = []

    # Fetch snowfall data
    snow_1_24hr = weather[resort1]["today"]["snow"]["24hr_snow"]
    snow_1_48hr = weather[resort1]["today"]["snow"]["48hr_snow"]
    snow_1_base = weather[resort1]["today"]["snow"]["base_snow"]

    snow_2_24hr = weather[resort2]["today"]["snow"]["24hr_snow"]
    snow_2_48hr = weather[resort2]["today"]["snow"]["48hr_snow"]
    snow_2_base = weather[resort2]["today"]["snow"]["base_snow"]

    # Compare snow data
    if snow_1_24hr > snow_2_24hr:
        if snow_1_48hr > snow_2_48hr:
            if snow_1_base > snow_2_base:
                clear_screen()
                return_statements.append(f"{resort1} has more snow in the last 24 hours, 48 hours, and a deeper base than {resort2}. \n{resort1} is likely to have the best ski conditions overall.")
            else:
                clear_screen()
                return_statements.append(f"{resort1} has more snow in the last 24 and 48 hours, but {resort2} has a deeper base. \n{resort1} may offer fresher conditions, while {resort2} has a more established base.")
        else:
            if snow_1_base > snow_2_base:
                clear_screen()
                return_statements.append(f"{resort1} has more snow in the last 24 hours and a deeper base, but {resort2} has more snow in the last 48 hours. \nConditions could be better at {resort1} due to the recent snow and base depth.")
            else:
                clear_screen()
                return_statements.append(f"{resort1} has more snow in the last 24 hours, but {resort2} has more snow in the last 48 hours and a deeper base. \n{resort2} might have better skiing conditions overall.")
    else:
        if snow_1_48hr > snow_2_48hr:
            if snow_1_base > snow_2_base:
                clear_screen()
                return_statements.append(f"{resort2} has more snow in the last 24 hours, but {resort1} has more snow in the last 48 hours and a deeper base. \n{resort1} might offer better overall skiing conditions.")
            else:
                clear_screen()
                return_statements.append(f"{resort2} has more snow in the last 24 hours, while {resort1} has more snow in the last 48 hours. However, {resort2} also has a deeper base. \n{resort2} may have better conditions overall.")
        else:
            if snow_1_base > snow_2_base:
                clear_screen()
                return_statements.append(f"{resort2} has more snow in the last 24 and 48 hours, but {resort1} has a deeper base. \nConditions might be better at {resort2} due to recent snow.")
            else:
                clear_screen()
                return_statements.append(f"{resort2} has more snow in the last 24 hours, 48 hours, and a deeper base. \n{resort2} is likely to have the best ski conditions overall.")


    # TODO: compare winds and gusts

    # TODO: compare visibility

    # TODO: compare temperatures

    return return_statements
    


def analysis():
    first_selection = choose_resort()
    second_selection = choose_resort()

    # use the numbers of the input to index the list. This converts the selectiosn to 
    # resort names with the proper formatting for the JSON it uses to access information.
    first_selection, second_selection = resorts_lst[int(first_selection - 1)], resorts_lst[int(second_selection - 1)]
    
    # now use these re-assaignments to grab the information and print to console. 
    # comparisons will hold a list of strings generated by check_weather()
    comparisons = check_weather(resort1=first_selection, resort2=second_selection)
    print('\n'.join(statement for statement in comparisons))
    again = cont()
    if not again:
        return False



def cont(option="Continue? (Y/N) "):
    done = False
    while not done:
        try:
            choice = input(f"\n{option}")
            if choice:
                if choice == "Y" or choice == 'y':
                    done = True
                    return True
                elif choice == "N" or choice == 'n':
                    clear_screen()
                    done = True
                    return False
                else: # invalid input
                    print("Invalid input! Enter 'Y' or 'N'!")
                    time.sleep(1)
                    clear_screen()
            else: # no input
                print("Invalid input! Input cannot be empty.")
                time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")


            
def overview():
    done = False

    while not done:
        clear_screen()
        res = choose_resort()
        if res == "q":
            done = False
            return False
        
        resort = resorts_lst[res - 1]

        print(f"{resort}:")
        print(f"    24 hr snow:     {weather[resort]['today']['snow']['24hr_snow']} inches")
        print(f"    48 hr snow:     {weather[resort]['today']['snow']['48hr_snow']} inches")
        print(f"    Today's temps:  {weather[resort]['today']['temps']['min_temp']}°F / {weather[resort]['today']['temps']['max_temp']}°F")
        print(f"    Avg wind:       {weather[resort]['today']['wind']['avg_wind']} mph")
        print(f"    Avg visibility: {int(weather[resort]['today']['vis']['avg_vis'])} ft")
        print(f"    Lift Report:    {weather[resort]['today']['snow']['lifts']} lifts running\n")

        if not cont(option="Check out another resort? (Y/N) "):
            break


def interface(score_dict):
    # TODO: remove top 3, replace analysis with compare, implement overall.
    done = False
    while not done:
        clear_screen()
        q_list = ["Welcome to the Ikon selector!", "(1) for top resort", "(2) for an overview", "(3) for comparing", "(q) to quit"]
        choice = validate_user_input(q_list=q_list, valid_inputs_lst=[1,2,3])
        if choice == "q":
            clear_screen()
            print("Exiting...")
            done = True

        elif choice == 1:
            print(f"The overall top resort is: {top_resort}")
            again = cont()
            if not again:
                done = True

        elif choice == 2:
            overview()

        elif choice == 3:
            analysis()
            

clear_screen()
interface(scores)

    


"""
--map--

(1) for top resort
(2) for an overview
(3) for comparing

overview ex:

Copper
    24 hr snow:
    48 hr snow:
    today's temps: high/low
    avg wind speed: 20 mph
    visibility:

"""