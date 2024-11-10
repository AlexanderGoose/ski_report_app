import requests
import json

ski_area_names = ['abasin', 'copper', 'steamboat', 'winter-park']

lift_reports = {'abasin': {},
                 'copper': {}, 
                 'steamboat': {},
                 'winter-park': {}}

def get_liftie_data(resort_name):
    base_url = "https://liftie.info/api/resort/"
    url = f"{base_url}{resort_name}"

    
    r = requests.get(url)
    if r.status_code == 200:
        resorts = r.text
        resorts = r.json()
        # print(json.dumps(resorts, indent=4))
        open = int(resorts['lifts']['stats']['open'])
        closed = int(resorts['lifts']['stats']['closed'])
        total_lifts = open + closed

        lift_reports[resort_name]['open'] = open
        lift_reports[resort_name]['closed'] = closed
        lift_reports[resort_name]['total_lifts'] = total_lifts
        # print(f"Lift report: {open} / {total_lifts} running")
    else:
        lift_reports[resort_name]['open'] = 'Error'
        lift_reports[resort_name]['closed'] = 'Error'
        lift_reports[resort_name]['total_lifts'] = 'Error'
       #  print(f"Error. Status code: {r.status_code}")

for resort in ski_area_names:
    get_liftie_data(resort)

with open('json_files/lift_reports.json', 'w') as file:
    json.dump(lift_reports, file, indent=4)


# get_liftie_data("copper")