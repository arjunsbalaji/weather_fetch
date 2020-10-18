from weather_au import api, summary
import sys, os
from pathlib import Path
import pandas as pd
from weather import place, observations
import time, requests, json, datetime


scarb_url = 'http://www.bom.gov.au/fwo/IDW60901/IDW60901.94614.json'
scarb_path = Path('./scarb/')

perth_url = 'http://www.bom.gov.au/fwo/IDW60901/IDW60901.94608.json'
perth_path = Path('./perth_metro/')

fetched_req = requests.get(url=scarb_url)
fetched_json = fetched_req.json();
blob = pd.json_normalize(fetched_json['observations']['data'])

def get_date_from_str(utc):
    return datetime.date(year = int(utc[0:4]),
                        month = int(utc[4:6]),
                        day = int(utc[6:8]))

while True:
    scarb_req = requests.get(url=scarb_url)
    scarb_json = scarb_req.json()
    scarb_dataframe = pd.json_normalize(scarb_json['observations']['data'])
    
    current_date = get_date_from_str(scarb_dataframe['local_date_time_full'][0])
    
    
    
    perth_req = requests.get(url=perth_url)
    perth_json = perth_req.json()
    perth_dataframe = pd.json_normalize(perth_json['observations']['data'])
    
    #save
    scarb_dataframe.to_csv(str(scarb_path/current_date.strftime("%m_%d_%Y")))
    perth_dataframe.to_csv(str(perth_path/current_date.strftime("%m_%d_%Y")))

    print('Scarborough Weather:' + str(scarb_dataframe['apparent_t'][0]))
    print('Perth Weather:' + str(perth_dataframe['apparent_t'][0]))
    time.sleep(86400)
