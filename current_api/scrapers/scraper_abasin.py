from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import json

weather_data = {'Arapahoe Basin': {}}

# ------------------- a basin
# only one that uses requests instead of session!
url_abasin = 'https://www.arapahoebasin.com/snow-report/'
r_abasin = requests.get(url_abasin)
if r_abasin.status_code == 200:
    soup = BeautifulSoup(r_abasin.content, 'html.parser') 
    past_24hr = soup.find_all('div', class_='value-box')[0].find('h5', class_='big-number').text.strip()
    past_48hr = soup.find_all('div', class_='value-box')[1].find('h5', class_='big-number').text.strip()
    base_snow = soup.find_all('div', class_='value-box')[2].find('h5', class_='big-number').text.strip()
    base_snow_fixed = base_snow.split('\u201d')[0]

    weather_data['Arapahoe Basin']['24hr_snow'] = int(past_24hr[:-1])
    weather_data['Arapahoe Basin']['48hr_snow'] = int(past_48hr[:-1])
    weather_data['Arapahoe Basin']['base_snow'] = int(base_snow_fixed)
else:
    print("Error occured for getting a basin data.")

file_path = 'json_files/scraped_data.json'

#open the JSON
with open(file_path, 'r') as file:
    existing_json = json.load(file)

# update the json with new resort
existing_json.update(weather_data)

# write the new json to the file to override
with open(file_path, 'w') as file:
    json.dump(existing_json, file, indent=4)

