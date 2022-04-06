# This script reads the scorecard data and fills in the missing values for the
# columns LATITUDE and LONGITUDE.  It does this by utilizing the geonames API.
# See https://www.geonames.org/export/web-services.html.  Since CITY and STABBR (state)
# are available for each college, we use that data to query the API.
# Note that we are limited to 1000 API requests per hour.  Some values are filled
# manually.

from urllib.request import urlopen
import pandas as pd
import json


na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
sc = pd.read_csv('data/temp1.csv', na_values=na_values)

username = 'team173'
url = 'http://api.geonames.org/search?maxRows=1&type=json&country=US&username=' + username
for i in sc.index:
    if pd.isnull(sc.loc[i, 'LATITUDE']) or pd.isnull(sc.loc[i, 'LONGITUDE']):
        query = '&q=' + sc.loc[i, 'CITY'].replace(' ', '+') + '+' + sc.loc[i, 'STABBR']
        response = urlopen(url + query)
        response_str = response.read()
        response_json = json.loads(response_str)
        try:
            if pd.isnull(sc.loc[i, 'LATITUDE']):
                sc.loc[i, 'LATITUDE'] = response_json['geonames'][0]['lat']
        except Exception:
            pass
        try:
            if pd.isnull(sc.loc[i, 'LONGITUDE']):
                sc.loc[i, 'LONGITUDE'] = response_json['geonames'][0]['lng']
        except Exception:
            pass
  
sc.to_csv('data/temp2.csv', index=False)