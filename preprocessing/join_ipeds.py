import pandas as pd


na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
colleges = pd.read_csv('../data/temp6.csv', na_values=na_values)
ipeds = pd.read_csv('../data/ipeds/ipeds.csv', na_values=na_values)

combined = pd.merge(colleges, ipeds, left_on='UNITID', right_on='UNITID', how='left')

combined.to_csv('../data/temp7.csv', index=False)