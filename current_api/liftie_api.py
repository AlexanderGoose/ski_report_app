import requests
import json

ski_area_names = ['abasin', 'copper', 'steamboat', 'winter-park']

lift_reports = {'abasin': {},
                 'copper': {}, 
                 'steamboat': {},
                 'winter-park': {}}

proxies = {
    "http": "http://72.10.160.91:9891" 
}

# connects to api, saves lift info to dictionary above
def get_liftie_data(resort_name):
    base_url = "https://liftie.info/api/resort/"
    url = f"{base_url}{resort_name}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r = requests.get(url, headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        resorts = r.text
        resorts = r.json()
        open = int(resorts['lifts']['stats']['open'])
        closed = int(resorts['lifts']['stats']['closed'])
        total_lifts = open + closed

        lift_reports[resort_name]['open'] = open
        lift_reports[resort_name]['closed'] = closed
        lift_reports[resort_name]['total_lifts'] = total_lifts
    else:
        lift_reports[resort_name]['open'] = 'Error'
        lift_reports[resort_name]['closed'] = 'Error'
        lift_reports[resort_name]['total_lifts'] = 'Error'

# runs the function for each resort
for resort in ski_area_names:
   get_liftie_data(resort)

# save lift info to json file
with open('json_files/lift_reports.json', 'w') as file:
   json.dump(lift_reports, file, indent=4)