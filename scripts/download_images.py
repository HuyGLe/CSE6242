from urllib.request import urlopen, urlretrieve
from urllib.parse import quote
import pandas as pd
import json


na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
colleges = pd.read_csv('../data/scorecard/temp4.csv', na_values=na_values)

endpoint = 'https://en.wikipedia.org/w/api.php'
for i in range(colleges.shape[0]):
    # get pageid
    college_name = quote(colleges.INSTNM[i])
    response1 = urlopen(endpoint + '?action=query&list=search&srlimit=1&srsearch=' + college_name).read()
    response_json1 = json.loads(response1)
    pageid = response_json1['query']['search'][0]['pageid']
    
    # get image url
    response2 = json.loads(urlopen(endpoint + '?action=query&prop=pageimages&pithumbsize=400&pageids=' + pageid))
    response_json2 = json.loads(response2)
    image_url = response_json2['query']['pages'][str(pageid)]['thumbnail']['source']
    
    # download image
    image_ext = image_url.split('.')[-1]
    urlretrieve(image_url, '../data/colleges/' + colleges.UNITID[i] + image_ext)