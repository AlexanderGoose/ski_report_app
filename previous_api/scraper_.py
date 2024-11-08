from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import json
import time

# Start the timer
start_time = time.time()

# TODO: add in temperature data with the scrapes
# TODO: add in wind data with the scrapes

session = HTMLSession()

urls = ['https://www.steamboat.com/the-mountain/mountain-report',
        'https://www.winterparkresort.com/the-mountain/mountain-report']

# # set up blank dict, this will be converted to a JSON output
weather_data = {'steamboat': {},
                'winter park': {},
                'a basin': {},
                'copper': {}}

# ------------------- steamboat and winter park
# they have the same class names and web structure! :)
for link in urls:
    if 'steamboat' in link:
        curr_res = 'steamboat'
    elif 'winterpark' in link:
        curr_res = 'winter park'

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

    weather_data[curr_res]['24 hr'] = past_24hr[:-1]
    weather_data[curr_res]['48 hr'] = past_48hr[:-1]
    weather_data[curr_res]['base']  = base_snow


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

    weather_data['a basin']['24 hr'] = past_24hr[:-1]
    weather_data['a basin']['48 hr'] = past_48hr[:-1]
    weather_data['a basin']['base']  = base_snow_fixed
else:
    print("Error occured for getting a basin data.")


# ------------------- copper mountain
# url_copper = 'https://www.coppercolorado.com/the-mountain/conditions-weather/snow-report'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }
# response_copper = session.get(url_copper, headers=headers)

# # This renders JavaScript content!! The whole point of using this!
# response_copper.html.render(timeout=30)

# # Get the rendered HTML content
# html_content_copper = response_copper.html.html
# soup = BeautifulSoup(html_content_copper, 'html.parser')
# values_copper = soup.find_all('p', class_='styles__ItemValue-sc-1kqptpn-12 ljFLoI')
# # print(values_copper)
# if values_copper:
#     past_24hr_copper = values_copper[2].text.strip()
#     past_48hr_copper = values_copper[2].text.strip()
#     base_snow_copper = values_copper[0].text.strip()
#     weather_data['copper']['24 hr'] = past_24hr_copper[:-1] # the [:-1] removes the " sign
#     weather_data['copper']['48 hr'] = past_48hr_copper[:-1]
#     weather_data['copper']['base']  = base_snow_copper[:-1]
# else:
#     print("Error occured getting data for Copper.")

url_copper = 'https://www.onthesnow.com/colorado/copper-mountain-resort/skireport'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response_copper = session.get(url_copper, headers=headers)
response_copper.html.render(timeout=30)
html_content_copper = response_copper.html.html
soup = BeautifulSoup(html_content_copper, 'html.parser')
values_copper = soup.find_all('span', class_='styles_snow__5Bl0_')
past_24hr_copper = values_copper[5].text.strip()
past_48hr_copper = values_copper[5].text.strip()
base_snow_copper = soup.find('div', class_='styles_metricNumber__54sKz').text.strip()
weather_data['copper']['24 hr'] = past_24hr_copper[:-1] # the [:-1] removes the " sign
weather_data['copper']['48 hr'] = past_48hr_copper[:-1]
weather_data['copper']['base']  = base_snow_copper[:-1]


with open("scraped_data.json", "w") as file:
    json.dump(weather_data, file, indent=4)

# End the timer
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")