from urllib.request import urlopen
import numpy as np
import pandas as pd
import json


na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
colleges = pd.read_csv('../data/temp3.csv', na_values=na_values)

url = 'http://climateapi.scottpinkelman.com/api/v1/location/'

colleges['CLIMATE_ZONE'] = np.nan

for i in colleges.index:
    try:
        response = urlopen(url + str(colleges.loc[i, 'LATITUDE']) + '/' + str(colleges.loc[i, 'LONGITUDE']))
        response_str = response.read()
        response_json = json.loads(response_str)
        colleges.loc[i, "CLIMATE_ZONE"] = response_json['return_values'][0]['koppen_geiger_zone']
    except Exception:
        pass
 
colleges.to_csv('../data/temp4.csv', index=False)