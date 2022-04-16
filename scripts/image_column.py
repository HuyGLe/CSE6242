import pandas as pd
import os


na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
colleges = pd.read_csv('../data/temp4.csv', na_values=na_values)

colleges['IMAGE'] = 'default.png'

images = os.listdir('../assets/images/colleges/')

for i in range(len(images)):
    unitid, ext = images[i].split('.')
    if unitid == 'default':
        continue
    else:
        colleges.loc[colleges.UNITID == int(unitid), 'IMAGE'] = unitid + ext

colleges.to_csv('../data/temp5.csv', index=False)