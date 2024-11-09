from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup

urls = ['https://www.arapahoebasin.com/snow-report/',
        'https://www.winterparkresort.com/the-mountain/mountain-report']  

# winter park
# past_24hr = soup.find_all('p', class_='LabeledItem_component__hgsZz')[1].find('strong').text.strip()
# past_48hr = soup.find_all('p', class_='LabeledItem_component__hgsZz')[2].find('strong').text.strip()
# base_snow = soup.find('h2', class_='LabelUnitToggle_labelUnitToggle_h0rp5')
driver = webdriver.Chrome()
url = 'https://www.winterparkresort.com/the-mountain/mountain-report'
driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'LabeledItem_component__hgsZz'))
)

# Get page source after content is loaded
page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

elements = soup.find_all('p', class_='LabeledItem_component__hgsZz')
print(len(elements))

# for elem in elements:
  #  print(elem.text.strip())

past_24hr = soup.find_all('p', class_='LabeledItem_component__hgsZz')[6].find('strong').text.strip()
print(past_24hr.split()[-1])
# Send a request to fetch the HTML content
# response = requests.get(url)
# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, 'html.parser')

    # Find the containers for the snow data based on classes shown in the HTML
    # past_24hr = soup.find_all('div', class_='value-box')[0].find('h5', class_='big-number').text.strip()
    # past_48hr = soup.find_all('div', class_='value-box')[1].find('h5', class_='big-number').text.strip()
    # base_snow = soup.find_all('div', class_='value-box')[2].find('h5', class_='big-number').text.strip()
    
    #past_24hr = soup.find('div', class_='WeatherCard_list__FfTEF').find('li')
    # ast_24hr = soup.find_all('p', class_='LabeledItem_component__hgsZz')[1].find('strong').text.strip()
    # past_48hr = soup.find_all('p', class_='LabeledItem_component__hgsZz')[2].find('strong').text.strip()
    # base_snow = soup.find('h2', class_='LabelUnitToggle_labelUnitToggle_h0rp5')
    # soup.prettify() > soup.html
    # # Print the extracted values
    # print(f"Past 24hr Snow: {past_24hr}")
    # print(f"Past 48hr Snow: {past_48hr}")
    # print(f"Base Snow: {base_snow}")

# else:
#     print(f"Failed to retrieve data. Status code: {response.status_code}")

    # TODO: create a folder with JSON's of ski resort class info
    # for each feature. THen loop thruogh and use beautiful soup to 
    # extract the info into a new JSON.

    # TODO: determine what I really want to find
    # 1) past 24 hr snow, 48 hr snow, 1 week if possible? 
    # 2) base snow depth
    # 3) might be able to pull high and low temps as well. If not, keep using open-meteo
    # 4) use open metro for visibility, temps, and maybe keep wind in there. 
    # 5) use liftie api to determine percent of lifts running

driver.quit()
