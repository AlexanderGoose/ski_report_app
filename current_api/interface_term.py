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


def clear_screen():
    os.system('clear')

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

# validate_user_input(q_list=['1 for a, 2 for b'], valid_inputs_lst=[1,2,3])

# TODO: add in analysis which allows a user to look into the weather data
# will allow the user to compare multiple resorts to one another
def analysis():
    # clear_screen()
    # print("How would you like to analyze?")
    # print("Type 1 to compare")
    # print("Type 2 to check a resort")
    # choice = input("\n>> ")
    what_to_analyze_lst = ["How would you like to analyze?", "Type 1 to compare","Type 2 to check a resort"]
    choice = validate_user_input(q_list=what_to_analyze_lst,
                                 valid_inputs_lst=[1, 2])

    def choose_resort(order):
        # TODO: rework this to fit into validate_user_input function!!!
        """returns a number (1 - 5).\n input is string, ex: 'first', uses it in input print statement"""
        while True:
            try:
                selection = input(f"Enter {order} resort >> ")
                if selection:
                    selection = int(selection)
                    valid_inputs = [1,2,3,4,5]
                    if selection not in valid_inputs:
                        print("Invalide input, try again.")
                        time.sleep(1)
                    else:
                        return selection
                else:
                    print("Invalid input, try again")
                    time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")
    
    def check_weather(resort1, resort2):

        """uses weather JSON to pull out data. Compares the data of two\n 
        resorts and makes assumptions based on comparisons."""

        # area to store explenations of weather
        return_statements = []

        snow_1_today = weather[resort1]["today"]["snow"]["total_snow"]
        snow_1_3     = weather[resort1]["three_day"]["snow"]["total_snow"]
        snow_1_7     = weather[resort1]["seven_day"]["snow"]["total_snow"]

        snow_2_today = weather[resort2]["today"]["snow"]["total_snow"]
        snow_2_3     = weather[resort2]["three_day"]["snow"]["total_snow"]
        snow_2_7     = weather[resort2]["seven_day"]["snow"]["total_snow"]

        # compares all combiantions of snow data
        # TODO: move all clear_screen() calls out of each conditional
        if snow_1_today > snow_2_today:
            if snow_1_3 > snow_2_3:
                if snow_1_7 > snow_2_7:
                    clear_screen()
                    return_statements.append(f"{resort1} has more snow today, in the last 3 days, and in the last 7 days. \n{resort1} is likely to have the best ski conditions.")
                else:
                    clear_screen()
                    return_statements.append(f"{resort1} has more snow today and in the last 3 days, but {resort2} has more snow in the last 7 days. \n{resort1} may have better conditions due to recent accumulation.")
            else:
                if snow_1_7 > snow_2_7:
                    clear_screen()
                    return_statements.append(f"{resort1} has more snow today and in the last 7 days, but {resort2} has had more snow in the last 3 days. \n{resort1} could still be better for skiing today due to fresh snow and overall buildup.")
                else:
                    clear_screen()
                    return_statements.append(f"{resort1} has more snow today, but {resort2} has had more snow in the last 3 and 7 days. \n{resort2} might have more consistent ski conditions from recent snow accumulation.")
        else:
            if snow_1_3 > snow_2_3:
                if snow_1_7 > snow_2_7:
                    clear_screen()
                    return_statements.append(f"{resort2} has more snow today, but {resort1} has more snow in the last 3 days and in the last 7 days. \n{resort1} might offer better overall skiing conditions from recent accumulation.")
                else:
                    clear_screen()
                    return_statements.append(f"While {resort1} has more snow in the last 3 days,{resort2} has more snow today and in the last 7 days. \nConditions could be balanced, but {resort1} might feel fresher from recent snow.")
            else:
                if snow_1_7 > snow_2_7:
                    clear_screen()
                    return_statements.append(f"{resort2} has more snow today and in the last 3 days, but {resort1} has more snow in the last 7 days. \n{resort2} may have better short-term conditions, while {resort1} might have deeper snow overall.")
                else:
                    clear_screen()
                    return_statements.append(f"{resort2} has more snow today, in the last 3 days, and in the last 7 days. \n{resort2} is likely to have the best ski conditions overall.")


        # TODO: compare winds and gusts

        # TODO: compare visibility

        # TODO: compare temperatures

        return return_statements
    
    # choice 1 is to compare. Prompt user to choose 2 resorts from list.
    if choice == 1:
        clear_screen()
        print("1 A Basin\n2 Copper\n3 Eldora\n4 Steamboat\n5 Winter Park\n")
        first_selection = choose_resort(order="first")
        second_selection = choose_resort(order="second")

        # use the numbers of the input to index the list. This converts the selectiosn to 
        # resort names with the proper formatting for the JSON it uses to access information.
        first_selection, second_selection = resorts_lst[int(first_selection - 1)], resorts_lst[int(second_selection - 1)]
        
        # now use these re-assaignments to grab the information and print to console. 
        # comparisons will hold a list of strings generated by check_weather()
        comparisons = check_weather(resort1=first_selection, resort2=second_selection)
        print('\n'.join(statement for statement in comparisons))

    elif choice == 2:
        # TODO: give the option to choose resort, then option to check an individual piece of information
        # instead of continue, let them check another piece of info or continue on
        clear_screen()

        def analyze_one_resort():
            # 1 - ask which resort to check, find the num, then grab it from the index
            print("1 A Basin\n2 Copper\n3 Eldora\n4 Steamboat\n5 Winter Park\n")
            selection = choose_resort(order="a")
            res = resorts_lst[int(selection - 1)]
            clear_screen()

            # 2 - check time frame
            time_frame_q_lst = ["Type 1 for today",
                                "Type 3 for past 3 days",
                                "Type 7 for last week",
                                "Type 0 to check all (NOT IMPLEMENTED)"]
            time = validate_user_input(q_list=time_frame_q_lst, valid_inputs_lst=[1, 3, 7, 0])

            if time == 1:
                time = "today"
            elif time == 3:
                time = "three_day"
            elif time == 7:
                time = "seven_day"
            elif time == 0:
                pass

            # 3 - prompt user to choose feature they want to check
            feature_q_list = ["Type 1 to check snowfall", 
                              "Type 2 to check visibility", 
                              "Type 3 to check temperature", 
                              "Type 4 to check wind/gusts", 
                              "Type 5 to check all (NOT IMPLEMENTED"]
            feature = validate_user_input(q_list=feature_q_list, valid_inputs_lst=[1, 2, 3, 4, 5])

            # 4 - grab the information
            if feature == 1:
                return f"Snowfall at {res}: {weather[res][time]['snow']['total_snow']} inches."
            if feature == 2:
                return f"Visibility at {res}: {weather[res][time]['vis']['avg_vis']} miles(?)."
            if feature == 3: # add additional selection to choose min, max
                return f"Temperature at {res}: {weather[res][time]['temps']['avg']} F (avg)."

        result = analyze_one_resort()
        print(result)
    # # invlaid input just recalls the function
    # else:
    #     print("invalid input")
    #     time.sleep(1)
    #     analysis()


def cont():
    while True:
        try:
            choice = input("\nContinue? (Y/N): ")
            if choice:
                if choice == "Y" or choice == 'y':
                    return True
                elif choice == "N" or choice == 'n':
                    print("exiting...")
                    clear_screen()
                    return False
                else: # invalid input
                    print("Invalid input! Enter 'Y' or 'N'!")
                    time.sleep(1)
                    clear_screen()
            else: # no input
                print("Invalid input! Input cannot be empty.")
                time.sleep(1)
            # make this not an inf loop
        except Exception as e:
            print(f"Error: {e}")


# set conndition for while loop, other functions can break out of it by setting this to false
# done = True 
def interface(score_dict):
    done = False
    while not done:
        clear_screen()
        print("Welcome to the Ikon selector!")
        print("Type 1 for top resort")
        print("Type 3 for top 3 resorts")
        print("Type 0 for worst resort")
        print("Type 5 for all")
        print("Type 7 for analysis\n")

        while True:
            try:
                first_selection = int(input(">> "))
                valid_inputs = [1, 3, 0, 5, 7]
                if first_selection and first_selection in valid_inputs:
                    if first_selection == 1:
                        clear_screen()
                        print(f"The overall top resort is: {top_resort}")
                    elif first_selection == 3:
                        clear_screen()
                        print("\n".join(f"{i + 1}: {resort}" for i, resort in enumerate(top_three))) # enumerate keeps track of position in list, i + 1 so it doesn't start at zero
                    elif first_selection == 0:
                        clear_screen()
                        print(f"The overall worst resort is: {worst}")
                    elif first_selection == 5:
                        clear_screen()
                        # prints all scores, * 100 to make more readable
                        print("\n".join(f"{i + 1}. {resort}: {int(score * 100)}" for i, (resort, score) in enumerate(scores.items())))
                    elif first_selection == 7:
                        analysis()
                    break
                else: # no input
                    print("Invalid input.")
                    time.sleep(1)
            except Exception as e:
                print(f"Invalid input.")
                time.sleep(1)

        # if cont returns T, done stays F
        # if cont returns F, then done goes to T
        done = not cont()
            

clear_screen()
interface(scores)