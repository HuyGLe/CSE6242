import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


## Maps degree name to column
def degree_dicts(df, columns):
    temp_col = columns[columns['VARIABLE NAME'].str.contains('CIP')]
    var_name = temp_col['VARIABLE NAME']
    var_name = var_name.astype('string')

    degs = temp_col['NAME OF DATA ELEMENT'].str.split('Bachelor\'s degree in ', expand=True).iloc[:,1]
    degs = degs.str.split('.', expand=True).iloc[:,0]
    degs = degs.astype('string')
    return dict(zip(degs, var_name))

## Custom distance metric
def custom_dist(x, y, weights):
    sum_dist = 0
    for i in range(len(x)):
        sum_dist += weights[i]*(x[i] - y[i])**2
    return np.sqrt(sum_dist)

## Read in files
data = pd.read_csv('data/final.csv')
norm = pd.read_csv('data/final_standardized.csv')

zip_to_state = pd.read_csv('data/zip_to_state.csv')
columns = pd.read_excel('data/scorecard/columns-simplified.xlsx')

## Create selectivity column (MOVED TO PREPROCESSING)
#select_col = np.zeros(len(norm))
#temp = norm[['ADM_RATE_ALL', 'GPA_BOTTOM_TEN_PERCENT']]
#for i in range(len(norm)):
#    select_col[i] += 0.3*-1*temp.iloc[i, 0] + 0.7*temp.iloc[i, 1]
#norm['SELECT'] = select_col

## Create teaching quality column (MOVED TO PREPROCESSING)
#teach_qual_col = np.zeros(len(norm))
#temp = norm[['INEXPFTE', 'AVGFACSAL', 'PFTFAC']]
#for i in range(len(norm)):
#    teach_qual_col[i] += 0.25*temp.iloc[i, 0] + 0.60*temp.iloc[i, 1] + 0.15*temp.iloc[i, 2]
#norm['TEACH_QUAL'] = teach_qual_col

def similar_colleges(college_id, weights):
    query = norm.iloc[data[data['UNITID'] == college_id].index,:].drop('UNITID', axis=1)
    weights = pd.DataFrame(weights).T
    for col in norm.drop('UNITID', axis=1):
        if col not in weights.columns:
            weights[col] = 3
    weights = weights[query.columns]
    weights = list(weights.T.iloc[:,0])
    neigh = NearestNeighbors(metric=custom_dist, metric_params = {'weights': weights})
    neigh.fit(norm.drop('UNITID', axis=1))
    return data.iloc[neigh.kneighbors(query, 4, return_distance=False)[0][1:], ]

def submit_form(school_dict, zipcode):
    ## Dictionaries to map size/cost references to numerical values
    size_ref = {1: 2500, 2: 5000, 3: 7500, 4: 10000, 5: 15000}
    cost_ref = {1: 2500, 2: 10000, 3: 20000, 4: 35000, 5: 50000}
    school_dict['UGDS'][0] = (size_ref[school_dict['UGDS'][0]] - np.mean(data.UGDS)) / np.std(data.UGDS)
    school_dict['TUITION'][0] = cost_ref[school_dict['TUITION'][0]]
    school_dict['TEACH_QUAL'][0] = max(norm['TEACH_QUAL'])
    school_dict['SELECT'][0] = max(norm['SELECT'])
    
    ## Penalize teach_qual, and select
    school_dict['TEACH_QUAL'][1]
    school_dict['SELECT'][1]
    
    user_state = zip_to_state[(zip_to_state['Zip Min'] <= zipcode) & (zip_to_state['Zip Max'] >= zipcode)].iloc[0, 0]
    
    ## Create custom tuition column based on in-state and out-of-state
    ## - modified to execute faster
    cost_col = data.TUITIONFEE_OUT.copy()
    cost_col.loc[data.STABBR == user_state] = data.TUITIONFEE_IN
    school_dict['TUITION'][0] = (school_dict['TUITION'][0] - np.mean(cost_col)) / np.std(cost_col)
    #data['TUITION'] = cost_col  # can't modify global dataframe
    std_cost_col = (cost_col - np.mean(cost_col)) / np.std(cost_col)
    #norm['TUITION'] = cost_col # can't modify global dataframe
    
    
    query = pd.DataFrame(pd.DataFrame(school_dict).iloc[0, :]).T
    
    non_stand_col = [col for col in query.columns if 'CLIMATE' in col or 'STABBR' in col]
    major_names = degree_dicts(data, columns).values()
    non_stand_col.append('TEACH_QUAL')
    non_stand_col.append('SELECT')
    non_stand_col.append('TUITION') # have to do this manually
    non_stand_col.extend([col for col in query.columns if col in major_names])

    for col in query.columns:
        if col in non_stand_col:
            continue
        mean = np.mean(data[col])
        std = np.std(data[col])
        query.loc[:, col] = (query[col] - mean) / std
            
    weights = pd.DataFrame(school_dict).iloc[1, :]
    
    cols = list(set(school_dict.keys()).difference(['TUITION']))
    norm_nn = norm[cols].copy()
    norm_nn['TUITION'] = std_cost_col
    norm_nn = norm_nn.loc[:, school_dict.keys()] # reorder columns to play well with neigh.fit() below
    
    neigh = NearestNeighbors(metric=custom_dist, metric_params = {'weights': weights})
    neigh.fit(norm_nn)
    
    return data.loc[neigh.kneighbors(query, len(data), return_distance=False)[0], ]

def filt(df, filter_col, filter_val, how):
    
    if df[filter_col].dtypes == np.dtype(object):
        return np.where(data[filter_col] == filter_val)
    else:
        if how == ">":
            return np.where(data[filter_col] > filter_val)
        elif how == ">=":
            return np.where(data[filter_col] >= filter_val)
        elif how == "<=":
            return np.where(data[filter_col] <= filter_val)
        elif how == "==":
            return np.where(data[filter_col] == filter_val)
        else:
            raise ValueError("Value for how should be one of >, >=, ==, <, <=")