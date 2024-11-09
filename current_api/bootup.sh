#!/bin/bash

clear

# echo "Loading..."

#progress bar
function progress_bar () {
    echo -ne "#          (10%)\r"
    sleep 2
    echo -ne "##         (20%)\r"
    sleep 2
    echo -ne "###        (30%)\r"
    sleep 2
    echo -ne "####       (40%)\r"
    sleep 2
    echo -ne "#####      (50%)\r"
    sleep 2
    echo -ne "######     (60%)\r"
    sleep 2
    echo -ne "#######    (70%)\r"
    sleep 1
    echo -ne "########   (80%)\r"
    sleep 1
    echo -ne "#########  (90%)\r"
    sleep 1
    echo -ne "########## (100%)\r"
}

# Start the progress bar in the background
# need to find a way to stop the function once all files are loaded
progress_bar &

(
    # 1 - get snow data
    # ./run_scraper.sh 

    # 2 - get main weather data
    python3 open-meteo.py 

    # combine the apis
    python3 combine_apis.py 
) &

wait

# 4 - Launch the interface
python3 interface_term.py



