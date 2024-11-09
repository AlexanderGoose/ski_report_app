from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import json
import time

session = HTMLSession()

weather_data = {'Copper': {}}

url_copper = 'https://www.onthesnow.com/colorado/copper-mountain-resort/skireport'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response_copper = session.get(url_copper, headers=headers)
if response_copper:
    response_copper.html.render(timeout=30)
    html_content_copper = response_copper.html.html
    soup = BeautifulSoup(html_content_copper, 'html.parser')
    values_copper = soup.find_all('span', class_='styles_snow__5Bl0_')
    past_24hr_copper = values_copper[5].text.strip()
    past_48hr_copper = values_copper[5].text.strip()
    base_snow_copper = soup.find('div', class_='styles_metricNumber__54sKz').text.strip()
    weather_data['Copper']['24 hr'] = past_24hr_copper[:-1] # the [:-1] removes the " sign
    weather_data['Copper']['48 hr'] = past_48hr_copper[:-1]
    weather_data['Copper']['base']  = base_snow_copper[:-1]
else:
    print("Error fetching data on Copper mountain.")

file_path = 'json_files/scraped_data.json'

#open the JSON
with open(file_path, 'r') as file:
    existing_json = json.load(file)

# update the json with new resort
existing_json.update(weather_data)

# write the new json to the file to override
with open(file_path, 'w') as file:
    json.dump(existing_json, file, indent=4)