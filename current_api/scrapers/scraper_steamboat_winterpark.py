from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json

session = HTMLSession()

urls = ['https://www.steamboat.com/the-mountain/mountain-report',
        'https://www.winterparkresort.com/the-mountain/mountain-report']

# # set up blank dict, this will be converted to a JSON output
weather_data = {'Steamboat': {},
                'Winter Park': {},}

# ------------------- steamboat and winter park
# they have the same class names and web structure! :)
for link in urls:
    if 'steamboat' in link:
        curr_res = 'Steamboat'
    elif 'winterpark' in link:
        curr_res = 'Winter Park'

    # session is an instance of HTMLSession from the requests_html library, 
    # which provides functionality for sending HTTP requests and rendering JavaScript.
    response = session.get(link)

    # This renders JavaScript content!! The whole point of using this!
    response.html.render(timeout=30)

    # Get the rendered HTML content
    html_content = response.html.html

    soup = BeautifulSoup(html_content, 'html.parser')

    past_24hr = soup.find_all('p', class_='LabeledItem_component__hgsZz')[5].find('strong').text.strip()
    past_48hr = soup.find_all('p', class_='LabeledItem_component__hgsZz')[6].find('strong').text.strip()
    base_snow = soup.find_all('h2', class_='LabelUnitToggle_label__PRGey')[1].text.strip()

    weather_data[curr_res]['24hr_snow'] = int(past_24hr[:-1])
    weather_data[curr_res]['48hr_snow'] = int(past_48hr[:-1])
    weather_data[curr_res]['base_snow'] = int(base_snow)


file_path = 'json_files/scraped_data.json'

#open the JSON
with open(file_path, 'r') as file:
    existing_json = json.load(file)

# update the json with new resort
existing_json.update(weather_data)

# write the new json to the file to override
with open(file_path, 'w') as file:
    json.dump(existing_json, file, indent=4)
