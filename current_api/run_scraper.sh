#!/bin/bash

echo "running scripts..."

# run 3 scraper files in parallel
python3 scraper_steamboat_winterpark.py &
python3 scraper_abasin.py &
python3 scraper_copper.py

# Wait for all background processes to finish before exiting
wait

echo "complete!"