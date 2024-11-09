import requests
import json

def get_liftie_data(resort_name):
    base_url = "https://liftie.info/api/resort/"
    url = f"{base_url}{resort_name}"

    
    r = requests.get(url)
    if r.status_code == 200:
        # resorts = r.text
        resorts = r.json()
        print(json.dumps(resorts, indent=4))
    else:
        print(f"Error. Status code: {r.status_code}")

get_liftie_data("big-sky")