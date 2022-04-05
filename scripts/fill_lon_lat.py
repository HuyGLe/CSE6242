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
 
sc.loc[6395, ['LATITUDE', 'LONGITUDE']] = [44.0580, -75.765752]
sc.loc[6473, ['LATITUDE', 'LONGITUDE']] = [44.545307, -72.000069]
sc.loc[6491, ['LATITUDE', 'LONGITUDE']] = [18.444247, -66.646407]
sc.loc[6492, ['LATITUDE', 'LONGITUDE']] = [18.3786, -65.8393]
sc.loc[6493, ['LATITUDE', 'LONGITUDE']] = [18.0111, -66.6141]
sc.loc[6494, ['LATITUDE', 'LONGITUDE']] = [18.2388, -66.0352]
sc.loc[6495, ['LATITUDE', 'LONGITUDE']] = [18.2013, -67.1452]
sc.loc[6578, ['LATITUDE', 'LONGITUDE']] = [18.2116, -65.7349]
sc.loc[6579, ['LATITUDE', 'LONGITUDE']] = [18.4704, -67.0242]
 
sc.to_csv('data/temp2.csv', index=False)