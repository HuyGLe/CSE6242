import pandas as pd
import numpy as np


na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'PrivacySuppressed']
colleges = pd.read_csv('../data/scorecard/Most-Recent-Cohorts-All-Data-Elements.csv', na_values=na_values)

cols = ['UNITID', 'INSTNM', 'CITY', 'STABBR', 'ZIP', 'INSTURL', 'MAIN',
         'NUMBRANCH', 'PREDDEG', 'HIGHDEG', 'CONTROL', 'REGION', 'LOCALE',
         'LATITUDE', 'LONGITUDE', 'CCBASIC', 'CCUGPROF', 'CCSIZSET', 'HBCU', 'PBI',
         'ANNHI', 'TRIBAL', 'AANAPII', 'HSI', 'NANTI', 'MENONLY', 'WOMENONLY', 'RELAFFIL',
         'ADM_RATE', 'ADM_RATE_ALL', 'SATVR25', 'SATVR75', 'SATMT25', 'SATMT75', 'SATVRMID',
         'SATMTMID', 'ACTCM25', 'ACTCM75', 'ACTEN25', 'ACTEN75', 'ACTMT25', 'ACTMT75',
         'ACTCMMID', 'ACTENMID', 'ACTMTMID', 'SAT_AVG', 'SAT_AVG_ALL', 'CIP01BACHL',
         'CIP03BACHL', 'CIP04BACHL', 'CIP05BACHL', 'CIP09BACHL', 'CIP10BACHL',
         'CIP11BACHL', 'CIP12BACHL', 'CIP13BACHL', 'CIP14BACHL', 'CIP15BACHL',
         'CIP16BACHL', 'CIP19BACHL', 'CIP22BACHL', 'CIP23BACHL', 'CIP24BACHL',
         'CIP25BACHL', 'CIP26BACHL', 'CIP27BACHL', 'CIP29BACHL', 'CIP30BACHL',
         'CIP31BACHL', 'CIP38BACHL', 'CIP39BACHL', 'CIP40BACHL', 'CIP41BACHL',
         'CIP42BACHL', 'CIP43BACHL', 'CIP44BACHL', 'CIP45BACHL', 'CIP46BACHL',
         'CIP47BACHL', 'CIP48BACHL', 'CIP49BACHL', 'CIP50BACHL', 'CIP51BACHL',
         'CIP52BACHL', 'CIP54BACHL', 'DISTANCEONLY', 'UGDS', 'UGDS_WHITE', 'UGDS_BLACK',
         'UGDS_HISP', 'UGDS_ASIAN', 'UGDS_AIAN', 'UGDS_NHPI', 'UGDS_2MOR', 'UGDS_NRA',
         'UGDS_UNKN', 'CURROPER', 'COSTT4_A', 'COSTT4_P', 'TUITIONFEE_IN',
         'TUITIONFEE_OUT', 'TUITFTE', 'INEXPFTE', 'AVGFACSAL', 'PFTFAC', 'UG25ABV',
         'COMP_ORIG_YR2_RT', 'COMP_ORIG_YR3_RT', 'COMP_ORIG_YR4_RT', 'COMP_ORIG_YR6_RT',
         'COMP_ORIG_YR8_RT', 'OPEFLAG' ,'ADMCON7', 'MDCOMP_ALL', 'UGDS_MEN',
         'UGDS_WOMEN', 'MD_EARN_WNE_P6', 'PCT25_EARN_WNE_P6', 'PCT75_EARN_WNE_P6',
         'COUNT_NWNE_1YR', 'COUNT_WNE_1YR', 'BOOKSUPPLY', 'ROOMBOARD_ON',
         'OTHEREXPENSE_ON', 'ROOMBOARD_OFF', 'OTHEREXPENSE_OFF', 'NPT4_PUB', 'NPT4_PRIV',
         'NPT41_PUB', 'NPT42_PUB', 'NPT43_PUB', 'NPT44_PUB', 'NPT45_PUB', 'NPT41_PRIV',
         'NPT42_PRIV', 'NPT43_PRIV', 'NPT44_PRIV', 'NPT45_PRIV', 'C150_4', 'OVERALL_YR6_N']
colleges = colleges.loc[:, cols]

# remove inactive colleges
colleges = colleges.loc[colleges.CURROPER == 1, :]
# remove colleges whose highest degree offered is less that a bachelor's
colleges = colleges.loc[colleges.HIGHDEG.isin([3, 4]), :]
# remove colleges that only offer graduate degrees
colleges = colleges.loc[colleges.PREDDEG != 4]
# remove program-year colleges
colleges = colleges.loc[pd.isnull(colleges.COSTT4_P), :]

# combine the NPT4 PUB/PRIV columns since they are mutually exclusive
colleges['NPT4'] = np.where(colleges.CONTROL == 1, colleges.NPT4_PUB, colleges.NPT4_PRIV)
colleges['NPT41'] = np.where(colleges.CONTROL == 1, colleges.NPT41_PUB, colleges.NPT41_PRIV)
colleges['NPT42'] = np.where(colleges.CONTROL == 1, colleges.NPT42_PUB, colleges.NPT42_PRIV)
colleges['NPT43'] = np.where(colleges.CONTROL == 1, colleges.NPT43_PUB, colleges.NPT43_PRIV)
colleges['NPT44'] = np.where(colleges.CONTROL == 1, colleges.NPT44_PUB, colleges.NPT44_PRIV)
colleges['NPT45'] = np.where(colleges.CONTROL == 1, colleges.NPT45_PUB, colleges.NPT45_PRIV)

# remove unneeded columns
dropcols = ['NPT4_PUB', 'NPT41_PUB', 'NPT42_PUB', 'NPT43_PUB', 'NPT44_PUB',
            'NPT45_PUB', 'NPT4_PRIV', 'NPT41_PRIV', 'NPT42_PRIV', 'NPT43_PRIV',
            'NPT44_PRIV', 'NPT45_PRIV', 'CURROPER', 'HIGHDEG', 'PREDDEG',
            'COSTT4_P']
colleges = colleges.drop(dropcols, axis=1)

# create missing dataframe to indicate which values are missing
missing = pd.isnull(colleges)
missing['COST_INSTATE_ONCAMPUS'] = missing.BOOKSUPPLY | missing.ROOMBOARD_ON | missing.OTHEREXPENSE_ON | missing.TUITIONFEE_IN
missing['COST_INSTATE_OFFCAMPUS'] = missing.BOOKSUPPLY | missing.ROOMBOARD_OFF | missing.OTHEREXPENSE_OFF | missing.TUITIONFEE_IN
missing['COST_OUTSTATE_ONCAMPUS'] = missing.BOOKSUPPLY | missing.ROOMBOARD_ON | missing.OTHEREXPENSE_ON | missing.TUITIONFEE_OUT
missing['COST_OUTSTATE_OFFCAMPUS'] = missing.BOOKSUPPLY | missing.ROOMBOARD_OFF | missing.OTHEREXPENSE_OFF | missing.TUITIONFEE_OUT
missing['FINAID1'] = missing.COSTT4_A | missing.NPT41
missing['FINAID2'] = missing.COSTT4_A | missing.NPT42
missing['FINAID3'] = missing.COSTT4_A | missing.NPT43
missing['FINAID4'] = missing.COSTT4_A | missing.NPT44
missing['FINAID5'] = missing.COSTT4_A | missing.NPT45
missing = missing.astype(int)
missing.to_csv('../data/missing.csv', index=False)

# set missing data for certain columns to default values
colleges.loc[pd.isnull(colleges.RELAFFIL), "RELAFFIL"] = -1

colleges.to_csv('../data/temp1.csv', index=False)