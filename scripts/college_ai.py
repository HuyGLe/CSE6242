from urllib.request import urlopen
import numpy as np
import pandas as pd
import json


na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
colleges = pd.read_csv('../data/temp2.csv', na_values=na_values)

key = '649ac8dea8e5eea6e723f1b76c'
url = 'https://api.collegeai.com/v1/api/college/info?api_key=' + key + '&college_unit_ids='
info_ids = '&info_ids=gpa_bottom_ten_percent'

colleges['GPA_BOTTOM_TEN_PERCENT'] = np.nan

for i in colleges.index:
    try:
        response = urlopen(url + str(int(colleges.loc[i, "UNITID"])) + info_ids)
        response_str = response.read()
        response_json = json.loads(response_str)
        if response_json['success'] == True:
            colleges.loc[i, "GPA_BOTTOM_TEN_PERCENT"] = response_json['colleges'][0]['gpaBottomTenPercent']
    except Exception:
        pass
 
colleges.to_csv('../data/temp3.csv', index=False)