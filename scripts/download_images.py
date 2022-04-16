from urllib.request import urlopen, urlretrieve
from urllib.parse import quote
import pandas as pd
import json

import os
os.chdir('C:\\Users\\jbos1\\Desktop\\gatech\\CSE6242\\Project\\CSE6242\\scripts')

na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
colleges = pd.read_csv('../data/temp4.csv', na_values=na_values)

endpoint = 'https://en.wikipedia.org/w/api.php'
#for i in range(colleges.shape[0]):
for i in range(2247, colleges.shape[0]):
    print(i)
    try:
        # get pageid
        college_name = quote(colleges.INSTNM[i])
        response1 = urlopen(endpoint + '?action=query&format=json&list=search&srlimit=1&srsearch=' + college_name).read()
        response_json1 = json.loads(response1)
        pageid = str(response_json1['query']['search'][0]['pageid'])
        
        # get image url
        response2 = urlopen(endpoint + '?action=query&format=json&prop=pageimages&pithumbsize=400&pageids=' + pageid).read()
        response_json2 = json.loads(response2)
        image_url = response_json2['query']['pages'][pageid]['thumbnail']['source']
        
        # download image
        image_ext = image_url.split('.')[-1]
        urlretrieve(image_url, '../assets/images/colleges/' + str(colleges.UNITID[i]) + '.' + image_ext)
    except Exception:
        pass