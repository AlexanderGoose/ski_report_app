#!/bin/bash

echo "running scripts..."

# run 3 scraper files in parallel
python3 scrapers/scraper_steamboat_winterpark.py &
python3 scrapers/scraper_abasin.py &
python3 scrapers/scraper_copper.py

# Wait for all background processes to finish before exiting
wait

echo "complete!"