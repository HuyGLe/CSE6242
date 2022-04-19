import pandas as pd


na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
colleges = pd.read_csv('../data/temp5.csv', na_values=na_values)
weather = pd.read_csv('../data/weatherSummary.csv', na_values=na_values)

weather = weather.loc[:, ['unitId', 'DoesPlaceHavehotSummer', 'IsthePlaceHumid', 'IsthePlaceSunny', 'IsthePlaceRainy', 'IsthePlaceSnowy']]

combined = pd.merge(colleges, weather, left_on='UNITID', right_on='unitId', how='left')
combined.drop('unitId', axis=1, inplace=True)
combined.rename({'DoesPlaceHavehotSummer':'HOT_SUMMER', 'IsthePlaceHumid':'HUMIDITY', 'IsthePlaceSunny':'SUNNY', 'IsthePlaceRainy':'RAINY', 'IsthePlaceSnowy':'SNOWY'})

combined.to_csv('../data/temp6.csv', index=False)