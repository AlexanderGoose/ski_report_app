#!/bin/bash

clear

echo "Loading..."


(
    # 1 - get snow data
    # ./run_scraper.sh 

    # 2 - get main weather data
    python3 open-meteo.py 

    # 3 - get lift status
    python3 liftie_api.py

    # combine the apis
    python3 combine_apis.py 
) 

wait

# 4 - Launch the interface
# python3 interface_term.py



