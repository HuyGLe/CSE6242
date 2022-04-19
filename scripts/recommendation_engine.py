import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


# Allows school prototype to have a location
state_locations = {'Alabama':[32.457246,-87.001333],
                   'Alaska':[59.982504,-141.696261],
                   'Arizona':[34.098164,-111.378474],
                   'Arkansas':[34.533717,-92.649341],
                   'California':[36.771164,-119.923645],
                   'Colorado':[38.373249,-105.701209],
                   'Connecticut':[41.385058,-72.691110],
                   'Delaware':[38.840778,-75.527285],
                   'Florida':[28.180178,-81.732944],
                   'Georgia':[32.736467,-83.430273],
                   'Hawaii':[20.533366,-156.347348],
                   'Idaho':[43.796212,-114.431539],
                   'Illinois':[40.439981,-88.927725], 
                   'Indiana':[39.868994,-86.250044],
                   'Iowa':[41.830008,-93.536847],
                   'Kansas':[38.380423,-98.116705],
                   'Kentucky':[37.339593,-84.859990],
                   'Louisiana':[30.894370,-92.439437],
                   'Maine':[44.896094,-69.174339],
                   'Maryland':[39.179758,-76.604333],
                   'Massachusetts':[42.333509,-71.637425],
                   'Michigan':[42.997952,-84.577063],
                   'Minnesota':[45.638368,-94.669158],
                   'Mississippi':[32.551443,-89.646030],
                   'Missouri':[38.230989,-92.455400],
                   'Montana':[46.643151,-109.428679],
                   'Nebraska':[41.160736,-99.156919],
                   'Nevada':[37.884971,-116.084972],
                   'New Hampshire':[43.137070,-71.486630],
                   'New Jersey':[40.011839,-74.384694],
                   'New Mexico':[34.810044,-106.234586],
                   'New York':[42.284760,-74.777316],
                   'North Carolina':[35.397260,-78.874314],
                   'North Dakota':[47.243191,-100.489373], 
                   'Ohio':[39.936416,-82.799119],
                   'Oklahoma':[35.489000,-97.328830],
                   'Oregon':[43.975688,-121.389093],
                   'Pennsylvania':[40.395371,-76.337372],
                   'Rhode Island':[41.760898,-71.541453],
                   'South Carolina':[33.726625,-80.607608],
                   'South Dakota':[44.301576,-100.414295],
                   'Tennessee':[35.584363,-87.289269],
                   'Texas':[31.045092,-98.424326],
                   'Utah':[39.134323,-111.695674],
                   'Vermont':[43.732737,-72.778328],
                   'Virginia':[37.199706,-78.002001],
                   'Washington':[47.253136,-120.784224],
                   'West Virginia':[38.481545,-80.691394],
                   'Wisconsin':[44.186144,-89.477742],
                   'Wyoming':[42.869255,-107.700023]
}


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
data = pd.read_csv('data/final.csv', index_col='UNITID')
data['UNITID'] = data.index # UNITID is an index for performance reasons; also need as col for map
norm = pd.read_csv('data/final_standardized.csv', index_col='UNITID')
norm['UNITID'] = norm.index

zip_to_state = pd.read_csv('data/zip_to_state.csv')
columns = pd.read_excel('data/scorecard/columns-simplified.xlsx')

def similar_colleges(college_id, weights):
    query = norm.loc[college_id, :].drop('UNITID', axis=1)
    x = norm.drop('UNITID', axis=1)
    weights = pd.DataFrame(weights)
    print(weights)
    for col in x:
        if col not in weights.columns:
            weights[col] = 3
    weights = weights[query.columns]
    weights = list(weights.T.iloc[:,0])
    neigh = NearestNeighbors(metric=custom_dist, metric_params = {'weights': weights})
    neigh.fit(x)
    return data.iloc[neigh.kneighbors(query, 4, return_distance=False)[0][1:], ]

def submit_form(school_dict, zipcode):
    print(1)
    print(school_dict)
    ## Dictionaries to map size/cost references to numerical values
    size_ref = {1: 2500, 2: 5000, 3: 7500, 4: 10000, 5: 15000}
    school_dict['UGDS'][0] = size_ref[school_dict['UGDS'][0]]
    school_dict['TEACH_QUAL'][0] = max(norm['TEACH_QUAL'])
    school_dict['SELECT'][0] = max(norm['SELECT'])
    
    print(2)
    user_state = zip_to_state[(zip_to_state['Zip Min'] <= zipcode) & (zip_to_state['Zip Max'] >= zipcode)].iloc[0, 0]
    ## Create custom tuition column based on in-state and out-of-state
    ## - modified to execute faster 
    cost_col = data.TUITIONFEE_OUT.copy()
    cost_col.loc[data.STABBR == user_state] = data.TUITIONFEE_IN
    std_cost_col = (cost_col - np.mean(cost_col)) / np.std(cost_col)
    school_dict['TUITION'][0] = min(std_cost_col)
    
    query = pd.DataFrame(pd.DataFrame(school_dict).iloc[0, :]).T
    
    print(3)
    print(query)
    non_stand_col = [col for col in query.columns if col[0:12] == 'CLIMATE_ZONE' or col[0:6] == 'STABBR'] 
    major_names = degree_dicts(data, columns).values()
    non_stand_col.append('TEACH_QUAL')
    non_stand_col.append('SELECT')
    non_stand_col.append('TUITION') # have to do this manually
    non_stand_col.extend([col for col in query.columns if col in major_names])
    print(non_stand_col)
    print(4)
    for col in query.columns:
        print(col)
        if col in non_stand_col:
            continue
        mean = np.mean(data[col])
        std = np.std(data[col])
        query.loc[:, col] = (query.loc[:, col] - mean) / std
    print(5)
    print(query)     
    weights = pd.DataFrame(school_dict).iloc[1, :]
    cols = list(set(school_dict.keys()).difference(['TUITION']))
    norm_nn = norm[cols].copy()
    norm_nn['TUITION'] = std_cost_col
    norm_nn = norm_nn.loc[:, school_dict.keys()] # reorder columns to play well with neigh.fit() below 
    print(6)
    neigh = NearestNeighbors(metric=custom_dist, metric_params = {'weights': weights})
    neigh.fit(norm_nn)
    return data.iloc[neigh.kneighbors(query, norm_nn.shape[0], return_distance=False)[0], ]

def get_data(rows):
    return (data.loc[rows.index, :])[rows]

def filt(df, filter_col, filter_val, how):
    curr_mask = np.ones(len(df))
    for i in range(len(filter_col)):
        if df[filter_col[i]].dtypes == np.dtype(object):
            curr_mask = curr_mask & (df[filter_col[i]] == filter_val[i])
        else:
            if how[i] == ">":
                curr_mask = curr_mask & (df[filter_col[i]] > filter_val[i])
            elif how[i] == ">=":
                curr_mask = curr_mask & (df[filter_col[i]] >= filter_val[i])
            elif how[i] == "<=":
                curr_mask = curr_mask & (df[filter_col[i]] <= filter_val[i])
            elif how[i] == "<":
                curr_mask = curr_mask & (df[filter_col[i]] < filter_val[i])
            elif how[i] == "==":
                curr_mask = curr_mask & (df[filter_col[i]] == filter_val[i])
            else:
                raise ValueError("Value for how should be one of >, >=, ==, <, <=")
    return np.where(curr_mask)