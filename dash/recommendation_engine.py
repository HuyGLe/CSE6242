import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import haversine_distances
from scipy.spatial import KDTree


# Allows school prototype to have a location
state_to_coords = {'AL':[32.457246,-87.001333],
                   'AK':[59.982504,-141.696261],
                   'AZ':[34.098164,-111.378474],
                   'AR':[34.533717,-92.649341],
                   'CA':[36.771164,-119.923645],
                   'CO':[38.373249,-105.701209],
                   'CT':[41.385058,-72.691110],
                   'DE':[38.840778,-75.527285],
                   'FL':[28.180178,-81.732944],
                   'GA':[32.736467,-83.430273],
                   'HI':[20.533366,-156.347348],
                   'ID':[43.796212,-114.431539],
                   'IL':[40.439981,-88.927725], 
                   'IN':[39.868994,-86.250044],
                   'IA':[41.830008,-93.536847],
                   'KS':[38.380423,-98.116705],
                   'KY':[37.339593,-84.859990],
                   'LA':[30.894370,-92.439437],
                   'ME':[44.896094,-69.174339],
                   'MD':[39.179758,-76.604333],
                   'MA':[42.333509,-71.637425],
                   'MI':[42.997952,-84.577063],
                   'MN':[45.638368,-94.669158],
                   'MS':[32.551443,-89.646030],
                   'MO':[38.230989,-92.455400],
                   'MT':[46.643151,-109.428679],
                   'NE':[41.160736,-99.156919],
                   'NV':[37.884971,-116.084972],
                   'NH':[43.137070,-71.486630],
                   'NJ':[40.011839,-74.384694],
                   'NM':[34.810044,-106.234586],
                   'NY':[42.284760,-74.777316],
                   'NC':[35.397260,-78.874314],
                   'ND':[47.243191,-100.489373], 
                   'OH':[39.936416,-82.799119],
                   'OK':[35.489000,-97.328830],
                   'OR':[43.975688,-121.389093],
                   'PA':[40.395371,-76.337372],
                   'RI':[41.760898,-71.541453],
                   'SC':[33.726625,-80.607608],
                   'SD':[44.301576,-100.414295],
                   'TN':[35.584363,-87.289269],
                   'TX':[31.045092,-98.424326],
                   'UT':[39.134323,-111.695674],
                   'VT':[43.732737,-72.778328],
                   'VA':[37.199706,-78.002001],
                   'WA':[47.253136,-120.784224],
                   'WV':[38.481545,-80.691394],
                   'WI':[44.186144,-89.477742],
                   'WY':[42.869255,-107.700023]
}

majors = ["Agriculture, Agriculture Operations, And Related Sciences", "Natural Resources And Conservation", "Architecture And Related Services", "Area, Ethnic, Cultural, Gender, And Group Studies", "Communication, Journalism, And Related Programs", "Communications Technologies/Technicians And Support Services", "Computer And Information Sciences And Support Services", "Personal And Culinary Services", "Education", "Engineering", "Engineering Technologies And Engineering-Related Fields", "Foreign Languages, Literatures, And Linguistics",	"Family And Consumer Sciences/Human Sciences", "Legal Professions And Studies", "English Language And Literature/Letters", "Liberal Arts And Sciences, General Studies And Humanities", "Library Science", "Biological And Biomedical Sciences", "Mathematics And Statistics", "Military Technologies And Applied Sciences", "Multi/Interdisciplinary Studies",	"Parks, Recreation, Leisure, And Fitness Studies", "Philosophy And Religious Studies", "Theology And Religious Vocations", "Physical Sciences", "Science Technologies/Technicians", "Psychology", "Homeland Security, Law Enforcement, Firefighting And Related Protective Services", "Public Administration And Social Service Professions", "Social Sciences", "Construction Trades", "Mechanic And Repair Technologies/Technicians", "Precision Production", "Transportation And Materials Moving", "Visual And Performing Arts", "Health Professions And Related Programs", "Business, Management, Marketing, And Related Support Services", "History"]
factors = [1, .875, 1.25, .85, .95, 1, 1.05, .875, .875, 1.25, 1.175, .925, .875, 1.3, .9, .925, .975, 1.2, 1.05, 1.1, .875, .85, .9, .9, 1.15, 1.15, 1, 1, 1, .925, .95, .95, 1.025, .95, .825, 1.125, 1.05, .925]
majors_scale = dict(zip(majors, factors))

def act_to_sat(act): # implementation of the table at https://www.princetonreview.com/college-advice/act-to-sat-conversion
    table = [600, 680, 735, 780, 830, 875, 915, 955, 995, 1035, 1075, 1110, 1140, 1175, 1215, 1255, 1290, 1325, 1365, 1400, 1430, 1465, 1500, 1535, 1575, 1600]
    if act < 11:
        gpa = 550 / (11 - act)
    else:
        gpa = table[act - 11]
    return gpa

def rank_student(gpa, sat, act):
    sat_equiv = act_to_sat(act)
    sat = max(sat, sat_equiv)
    table = np.array([
        [8, 7, 6, 6, 5, 5],
        [8, 7, 6, 6, 5, 5],
        [7, 6, 6, 5, 4, 4],
        [6, 6, 5, 5, 4, 4],
        [6, 5, 4, 3, 3, 2],
        [6, 5, 4, 3, 2, 2],
        [6, 5, 4, 3, 2, 1]
    ])
    if gpa < 2:
        col = 0
    elif gpa <= 2.4:
        col = 1
    elif gpa <= 2.9:
        col = 2
    elif gpa <= 3.4:
        col = 3
    elif gpa <= 3.7:
        col = 4
    else:
        col = 5
    if sat < 940:
        row = 0
    elif sat <= 1050:
        row = 1
    elif sat <= 1160:
        row = 2
    elif sat <= 1270:
        row = 3
    elif sat <= 1380:
        row = 4
    else:
        row = 5
    return table[col, row]

def standardize(x, base=None):
    if base is None:
        return (x - np.mean(x)) / np.std(x)
    else:
        return (x-np.mean(base)) / np.std(base)

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
zip_to_coords = pd.read_csv('data/zip_to_coords.csv', index_col='ZIPCODE')
columns = pd.read_excel('data/columns-simplified.xlsx')

tree_kd = KDTree(data[['LATITUDE', 'LONGITUDE']])
def dist_to_lat(dist, unit='kilometers'):
    if unit == 'miles':
        dist *= 1.60934
        return dist*1.60934/110.574
    
def adjust_weights(school_dict):
    for key in school_dict.keys():
        weight = school_dict[key][1]
        if key == 'STABBR.':
            weight *= 3
        if weight == 5 or weight == 5*0.12 or weight == 5*0.4:
            weight *= 2.4
        elif weight == 1 or weight == 0.12 or weight == 0.4 or weight == 0.33:
            weight *= 0.15
        school_dict[key][1] = weight


def similar_schools(college_id):
    cols = ['ADM_RATE', 'SAT_AVG', 'UGDS', 'DIVERSITY', 'TEACH_QUAL', 'TUITIONFEE_IN',
            f'STABBR.{data.loc[college_id, "STABBR"]}',f'RELAFFIL.{data.loc[college_id, "RELAFFIL"]}',
            'GPA_BOTTOM_TEN_PERCENT', f'CLIMATE_ZONE_GROUP.{data.loc[college_id, "CLIMATE_ZONE_GROUP"]}',
            'EXP_EARNINGS', 'MAIN']
    weights= [1, 1, 1.5, 2, 3, 3, 2, 2.5, 1, 1, 3, 1]
    query = norm.loc[data[data['UNITID'] == college_id].index, cols]

    neigh = NearestNeighbors(metric=custom_dist, metric_params = {'weights': weights})
    neigh.fit(norm[cols])
    return data.iloc[neigh.kneighbors(query, 5, return_distance=False)[0][1:], ]

def submit_form(school_dict, user_info):
    print('submit_form()')
    print('school_dict:')
    print(school_dict)
    print('user_info:')
    print(user_info)
    size_ref = {1: 2500, 2: 5000, 3: 7500, 4: 10000, 5: 15000}
    school_dict['UGDS'][0] = standardize(size_ref[school_dict['UGDS'][0]], data.UGDS)
    school_dict['TEACH_QUAL'][0] = max(norm['TEACH_QUAL'])
    school_dict['SELECT'][0] = max(norm['SELECT'])
    school_dict['DIVERSITY'][0] = max(norm['DIVERSITY'])
    user_state = user_info['state']
    # TUITION
    cost_col = data.TUITIONFEE_OUT.copy()
    cost_col.loc[data.STABBR == user_state] = data.TUITIONFEE_IN
    std_cost_col = standardize(cost_col)
    school_dict['TUITION'][0] = min(std_cost_col)
    # EXP_EARNINGS
    exp_earnings_col = data.EXP_EARNINGS * majors_scale[user_info['major']] + data.EXP_EARNINGS_DROPOUT
    std_exp_earnings_col = standardize(exp_earnings_col)
    school_dict['EXP_EARNINGS'][0] = max(std_exp_earnings_col)
    # DISTANCE
    preferred_state = ''
    location_imp = 0
    for key in school_dict.keys():
        if key[0:7] == 'STABBR.':
            preferred_state = key[7:9]
            location_imp = school_dict[key][1]
    latitude, longitude = state_to_coords[preferred_state]
    lat_rad = np.radians(latitude)
    lon_rad = np.radians(longitude)
    distance_col = data.loc[:,['LAT_RAD', 'LON_RAD']].apply(lambda x: haversine_distances([[lat_rad, lon_rad], [x.LAT_RAD, x.LON_RAD]])[0, 1], axis=1)
    std_distance_col = standardize(distance_col)
    school_dict['DISTANCE'] = [min(std_distance_col), location_imp*0.33]
    # SELECTIVITY RANK DISTANCE
    student_rank = rank_student(user_info['gpa'], user_info['sat'], user_info['act'])
    rank_distance_col = student_rank - data.SELECT_CAT
    std_rank_distance_col = standardize(rank_distance_col)
    school_dict['RANK_DISTANCE'] = [0, 2.6]
    # ABHISHEK'S ORDINAL COLS
    for col in ['HOT_SUMMER', 'HUMIDITY', 'SUNNY', 'RAINY']:
        school_dict[col][0] = standardize(school_dict[col][0], data.loc[:, col])
    print('---------------------------')
    print('school_dict:')
    print(school_dict)
    adjust_weights(school_dict)
    query = pd.DataFrame(pd.DataFrame(school_dict).iloc[0, :]).T
    weights = pd.DataFrame(school_dict).iloc[1, :]
    # SET UP NN DATAFRAME
    cols = list(set(school_dict.keys()).difference(['TUITION', 'EXP_EARNINGS', 'DISTANCE', 'RANK_DISTANCE']))
    norm_nn = norm[cols].copy()
    norm_nn['TUITION'] = std_cost_col
    norm_nn['EXP_EARNINGS'] = std_exp_earnings_col
    norm_nn['DISTANCE'] = std_distance_col
    norm_nn['RANK_DISTANCE'] = np.where(rank_distance_col>0, np.abs(rank_distance_col)*2, np.abs(rank_distance_col))
    norm_nn = norm_nn.loc[:, school_dict.keys()] # reorder columns to play well with neigh.fit() below 
    print('adjusted school dict:')
    print(school_dict) # 110404 122296
    print('weights:')
    print(weights)
    print('query')
    print(query)
    print('SM:')
    print(norm_nn.loc[122296, :])
    print('DISTANCES')
    dist_sm = 0
    dist_cit = 0
    print(query.shape)
    print(weights.shape)
    for col in cols:
        print('-------------------------------------------------')
        print(col)
        print(weights[col])
        print(f'{query[col]} :: {norm_nn.at[122296, col]} :: {norm_nn.at[110404, col]}')
        dist_sm += weights[col]*(norm_nn.at[122296, col] - query[col])**2
        dist_cit += weights[col]*(norm_nn.at[110404, col] - query[col])**2
    print(f'dist cit: {dist_cit}')
    print(f'dist_sm: {dist_sm}')
    print('---- ----')
    print(norm_nn.iloc[0,:])
    #print(custom_dist(query,norm_nn.loc[110404,:].squeeze(),weights))
    # NN
    neigh = NearestNeighbors(metric=custom_dist, metric_params = {'weights': weights})
    neigh.fit(norm_nn)
    x = neigh.kneighbors(query, 1, return_distance=True)
    print(x)
    return data.iloc[neigh.kneighbors(query, norm_nn.shape[0], return_distance=False)[0], ]

def get_data(rows):
    return (data.loc[rows.index, :])[rows]

def get_all_data():
    return data, norm

def filt(local_df, filters, user_info):
    print('filt() - filters:')
    print(filters)
    df = data.loc[local_df.index, :]
    mask = pd.Series(np.ones(len(local_df), dtype=bool), index=local_df.index)
    col_filters = [[k,v] for k,v in filters.items() if v[1] != '*']
    for i in range(len(col_filters)):
        col = col_filters[i][0]
        val = col_filters[i][1][0]
        how = col_filters[i][1][1]
        if how == ">":
            mask &= (df.loc[:, col] > val)
        elif how == ">=":
            mask &= (df.loc[:, col] >= val)
        elif how == "<=":
            mask &= (df.loc[:, col] <= val)
        elif how == "<":
            mask &= (df.loc[:, col] < val)
        elif how == "==":
            mask &= (df.loc[:, col] == val)
        else:
            raise ValueError("Value for how should be one of >, >=, ==, <, <=")
    if 'DISTANCE' in filters and 'ZIP' in filters:
        coords = zip_to_coords.loc[filters['ZIP'][0], ['LATITUDE', 'LONGITUDE']]
        distance = filters['DISTANCE'][0]
        query_kd = tree_kd.query_ball_point(coords, dist_to_lat(distance, 'miles'))
        kd_mask = pd.Series(np.zeros(len(local_df), dtype=bool), index=local_df.index)
        kd_mask.loc[data.index[query_kd]] = np.ones(len(query_kd), dtype=bool)
        mask &= kd_mask
    if 'TUITION' in filters:
        min_tuition, max_tuition = filters['TUITION'][0]
        tuition = df.TUITIONFEE_OUT.copy()
        tuition.loc[df.STABBR == user_info['state']] = df.TUITIONFEE_IN
        mask &= (min_tuition <= tuition) & (tuition <= max_tuition)
    if 'EARNINGS' in filters:
        min_earnings, max_earnings = filters['EARNINGS'][0]
        earnings = df.EXP_EARNINGS * majors_scale[user_info['major']]
        mask &= (min_earnings <= earnings) & (earnings <= max_earnings)
    if 'SELECT_CAT' in filters:
        user_cat = rank_student(user_info['gpa'], user_info['sat'], user_info['act'])
        if 'Safety Schools' not in filters['SELECT_CAT'][0]:
            mask &= ~(user_cat + 2 <= df.SELECT_CAT)
        if '50/50 Schools' not in filters['SELECT_CAT'][0]:
            mask &= ~((user_cat - 1 <= df.SELECT_CAT) & (df.SELECT_CAT <= user_cat + 1))
        if 'Reach Schools' not in filters['SELECT_CAT'][0]:
            mask &= ~(user_cat - 2 >= df.SELECT_CAT)       
        
        
    df = df.loc[mask, :]
    mask = pd.Series(mask, local_df.index)
    return mask, df