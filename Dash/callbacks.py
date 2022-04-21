import json
import pandas as pd
import numpy as np
from dash import Input, Output, State, callback, html, dcc, callback_context
import plotly.express as px
import sys
sys.path.append('./scripts')
import recommendation_engine as rec
import front_end as fe

n = 12 # number of schools to list on page 2
state_to_stabbr = dict(zip(['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'], ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']))
stabbr_to_state = {v:k for k,v in state_to_stabbr.items()}
climate_zone_groups = {'Tropical (examples: Honolulu and Miami)':'A', 'Arid (examples: Pheonix and Denver)':'B', 'Temperate (examples: San Francisco and Atlanta)':'C', 'Continental (examples: Boston and Detroit)':'D'}
weather_type_to_col = {}
majors = ["Agriculture, Agriculture Operations, And Related Sciences", "Natural Resources And Conservation", "Architecture And Related Services", "Area, Ethnic, Cultural, Gender, And Group Studies", "Communication, Journalism, And Related Programs", "Communications Technologies/Technicians And Support Services", "Computer And Information Sciences And Support Services", "Personal And Culinary Services", "Education", "Engineering", "Engineering Technologies And Engineering-Related Fields", "Foreign Languages, Literatures, And Linguistics",	"Family And Consumer Sciences/Human Sciences", "Legal Professions And Studies", "English Language And Literature/Letters", "Liberal Arts And Sciences, General Studies And Humanities", "Library Science", "Biological And Biomedical Sciences", "Mathematics And Statistics", "Military Technologies And Applied Sciences", "Multi/Interdisciplinary Studies",	"Parks, Recreation, Leisure, And Fitness Studies", "Philosophy And Religious Studies", "Theology And Religious Vocations", "Physical Sciences", "Science Technologies/Technicians", "Psychology", "Homeland Security, Law Enforcement, Firefighting And Related Protective Services", "Public Administration And Social Service Professions", "Social Sciences", "Construction Trades", "Mechanic And Repair Technologies/Technicians", "Precision Production", "Transportation And Materials Moving", "Visual And Performing Arts", "Health Professions And Related Programs", "Business, Management, Marketing, And Related Support Services", "History"]
major_nums = ['01', '03', '04', '05', '09', '10', '11', '12', '13', '14', '15', '16', '19', '22', '23', '24', '25', '26', '27', '29', '30', '31', '38', '39', '40' ,'41', '42', '43', '44', '45' ,'46', '47' , '48', '49', '50', '51', '52', '54']
major_to_num = dict(zip(majors, major_nums))
locale_first_to_num = {'City':'1', 'Suburb':'2', 'Town':'3', 'Rural':'4'}
dcc.Dropdown(id='rainy-i', placeholder='Rain', options=['Desert', 'Low', 'Moderate', 'Rainy']),
hot_summer_to_level = {'Cool':1, 'Moderate':2, 'Warm':3, 'Hot':4}
humidity_to_level = {'Dry':1, 'Moderate':2, 'Humid':3, 'Very Humid':4}
sunny_to_level = {'Cloudy':1, 'Some Sun':2, 'Very Sunny':3}
rainy_to_level = {'Desert':1, 'Low':2, 'Moderate':3, 'Rainy':4}

##############################  Global ##############################
@callback(Output('new-page', 'data'),
          Output('last-page', 'data'),
          Input('url', 'pathname'),
          State('new-page', 'data'),
          State('last-page', 'data'))
def url_update(pathname, new_page, last_page):
    print(f'url_update() -- last-page:{last_page} , new-page:{new_page}')
    print('Changing to:')
    if pathname == '/1' or pathname == '/2' or pathname[1:8] == 'college' or pathname == '/2/filter' or pathname == '/2/filter0':
        print(f'last-page:{new_page} , new-page:{pathname}')
        return pathname, new_page
    else:
        return '/1', '/1'
    
    
##############################  Page 1 ##############################
@callback(Output('1s', 'data'),
          Input('major-i', 'value'),
          Input('zip-i', 'value'),
          Input('gpa-i', 'value'),
          Input('sat-i', 'value'),
          Input('act-i', 'value'),
          Input('state-i', 'value'),
          Input('state-imp', 'value'),
          Input('ugds-i', 'value'),
          Input('ugds-imp', 'value'),
          Input('locale-first-i', 'value'),
          Input('locale-first-imp', 'value'),
          Input('climate-zone-i', 'value'),
          Input('hot-summer-i', 'value'),
          Input('humidity-i', 'value'),
          Input('sunny-i', 'value'),
          Input('rainy-i', 'value'),
          Input('snowy-i', 'value'),
          Input('weather-imp', 'value'),
          Input('tuition-imp', 'value'),
          Input('select-imp', 'value'),
          Input('teach-qual-imp', 'value'),
          Input('exp-earnings-imp', 'value'),
          Input('diversity-imp', 'value'), prevent_initial_call=True)
def page_1_input(major, zipcode, gpa, sat, act, state, state_imp, ugds, ugds_imp, locale_first, locale_first_imp,
                 climate_zone, hot_summer, humidity, sunny, rainy, snowy, weather_imp, tuition_imp, select_imp,
                 teach_qual_imp, exp_earnings_imp, diversity_imp):
    form = dict()
    form['major-i'] = major
    form['zip-i'] = zipcode
    form['gpa-i'] = gpa
    form['sat-i'] = sat
    form['act-i'] = act
    form['state-i'] = state
    form['state-imp'] = state_imp
    form['ugds-i'] = ugds
    form['ugds-imp'] = ugds_imp
    form['locale-first-i'] = locale_first
    form['locale-first-imp'] = locale_first_imp
    form['climate-zone-i'] = climate_zone
    form['hot-summer-i'] = hot_summer
    form['humidity-i'] = humidity
    form['sunny-i'] = sunny
    form['rainy-i'] = rainy
    form['snowy-i'] = snowy
    form['weather-imp'] = weather_imp
    form['tuition-imp'] = tuition_imp
    form['select-imp'] = select_imp
    form['teach-qual-imp'] = teach_qual_imp
    form['exp-earnings-imp'] = exp_earnings_imp
    form['diversity-imp'] = diversity_imp
    return json.dumps(form)

##############################  Page 2 ############################## 
def filter_vals(filter_dict, reset):
    print('filter_vals() - filter_dict:')
    print(filter_dict)
    if reset == True:
        zip_ii = None
        distance = None
        state_ii = None
        tuition_ii = [0, 50000]
        applfeeu_ii = None
        exp_earnings_ii = [0, 125000]
        select_cat_ii = ['Safety Schools', '50/50 Schools', 'Reach Schools']
        climate_zone_ii = None
        hot_summer_ii = None
        humidity_ii = None
        sunny_ii = None
        rainy_ii = None
        snowy_ii = None
    else:
        zip_ii = filter_dict['zip-ii'] if 'zip-ii' in filter_dict else None
        distance = f'{filter_dict["distance"]} miles' if 'distance' in filter_dict else None
        state_ii =  filter_dict['state-ii'] if 'state-ii' in filter_dict else None
        tuition_ii = filter_dict['tuition-ii']
        applfeeu_ii = filter_dict['applfeeu-ii'] if 'applfeeu-ii' in filter_dict else None
        exp_earnings_ii = filter_dict['exp-earnings-ii']
        select_cat_ii = filter_dict['select-cat-ii'] if 'select-cat-ii' in filter_dict else None
        climate_zone_ii = filter_dict['climate-zone-ii'] if 'climate-zone-ii' in filter_dict else None
        hot_summer_ii = filter_dict['hot-summer-ii'] if 'hot-summer-ii' in filter_dict else None
        humidity_ii = filter_dict['humidity-ii'] if 'humidity-ii' in filter_dict else None
        sunny_ii = filter_dict['sunny-ii'] if 'sunny-ii' in filter_dict else None
        rainy_ii = filter_dict['rainy-ii'] if 'rainy-ii' in filter_dict else None
        snowy_ii = filter_dict['snowy-ii'] if 'snowy-ii' in filter_dict else None
    return [zip_ii, distance, state_ii, tuition_ii, applfeeu_ii, exp_earnings_ii, select_cat_ii, climate_zone_ii,
            hot_summer_ii, humidity_ii, sunny_ii, rainy_ii, snowy_ii]

def create_user_info_dict(form):
    info = dict()
    if form['major-i'] is None:
        info['major'] = 'Engineering'
    else:
        info['major'] = form['major-i']
    if form['gpa-i'] is None:
        info['gpa'] = 3
    else:
        info['gpa'] = form['gpa-i']
    if form['zip-i'] is None:
        info['zip'] = '02139'
    else:
        info['zip'] = form['zip-i']
    zipcode = int(info['zip'])
    info['state'] = rec.zip_to_state[(rec.zip_to_state['Zip Min'] <= zipcode) & (rec.zip_to_state['Zip Max'] >= zipcode)].iloc[0, 0]
    if form['act-i'] is None:
        info['act'] = 5
    else:
        info['act'] = form['act-i']
    if form['sat-i'] is None:
        info['sat'] = rec.act_to_sat(info['act'])
    else:
        info['sat'] = form['sat-i']
    return info

def fill_form(form, form_dict):
    if form['major-i'] is not None:
        form_dict[f'CIP{major_to_num[form["major-i"]]}BACHL'] = [1, 5]
    else:
        form_dict['CIP13BACHL'] = [1, 1]
    if form['state-i'] is not None:
        form_dict[f'STABBR.{state_to_stabbr[form["state-i"]]}'] = [1, int(form['state-imp'])]
    else:
        form_dict['STABBR.IL'] = [1, 1]
    form_dict['UGDS'] = [int(form['ugds-i']), int(form['ugds-imp'])] # Always has a value
    if form['locale-first-i'] is not None:
        form_dict[f'LOCALE_FIRST.{locale_first_to_num[form["locale_first"]]}'] = [1 , int(form['locale_first-imp'])]
    else:
        form_dict['LOCALE_FIRST.2'] = [1 , 1]
    if form['climate-zone-i'] is not None: 
        form_dict[f'CLIMATE_ZONE_GROUP.{climate_zone_groups[form["climate-zone-i"]]}'] = [1, int(form['weather-imp'])*.6]
    else:
        form_dict['CLIMATE_ZONE_GROUP.C'] = [1, 1]
    if form['hot-summer-i'] is not None:
        form_dict['HOT_SUMMER'] = [hot_summer_to_level[form['hot-summer-i']], int(form["weather-imp"])*.08]
    else:
        form_dict['HOT_SUMMER'] = [3, 1]
    if form['humidity-i'] is not None:
        form_dict['HUMIDITY'] = [humidity_to_level[form['humidity-i']], int(form["weather-imp"])*.08]
    else:
        form_dict['HUMIDITY'] = [2, 1]
    if form['sunny-i'] is not None:
        form_dict['SUNNY'] = [sunny_to_level[form['sunny-i']], int(form["weather-imp"])*.08]
    else:
        form_dict['SUNNY'] = [2, 1]
    if form['rainy-i'] is not None:
        form_dict['RAINY'] = [rainy_to_level[form['rainy-i']], int(form["weather-imp"])*.08]
    else:
        form_dict['RAINY'] = [1, 1]
    if form['snowy-i'] is not None:
        form_dict['SNOWY'] = [1 if form['snowy-i'] == 'Yes' else 0, form['weather-imp ']*.08]
    else:
        form_dict['SNOWY'] = [1, 1]
    form_dict['TUITION'] = [None, int(form['tuition-imp'])]
    form_dict['SELECT'] = [None, int(form['select-imp'])]
    form_dict['TEACH_QUAL'] = [None, int(form['teach-qual-imp'])]
    form_dict['EXP_EARNINGS'] = [None, int(form['exp-earnings-imp'])]
    form_dict['DIVERSITY'] = [None, int(form['diversity-imp'])]

def prepare_filters(filter_dict):
    new_dict = {}
    if 'zip-ii' in filter_dict:
        new_dict['ZIP'] = [filter_dict['zip-ii'], '*']
    if 'distance' in filter_dict:
        new_dict['DISTANCE'] = [int(filter_dict['distance'].split(' ')[0]), '*']
    if 'state-ii' in filter_dict:
        new_dict['STABBR'] = [state_to_stabbr[filter_dict['state-ii']], '==']
    if 'tuition-ii' in filter_dict:
        new_dict['TUITION'] = [filter_dict['tuition-ii'], '*']
    if 'applfeeu-ii' in filter_dict:
        new_dict['APPLFEEU'] = [filter_dict['applfeeu-ii'], '<=']
    if 'exp-earnings-ii' in filter_dict:
        new_dict['EARNINGS'] = [filter_dict['exp-earnings-ii'], '*']
    if 'select-cat-ii' in filter_dict:
        new_dict['SELECT_CAT'] = [filter_dict['select-cat-ii'], '*']
    if 'climate-zone-ii' in filter_dict:
        if filter_dict['climate-zone-ii'] == 'Tropical':
            level = 'A'
        elif filter_dict['climate-zone-ii'] == 'Arid':
            level = 'B'
        elif filter_dict['climate-zone-ii'] == 'Temperate':
            level = 'C'
        else:
            level = 'D'
        new_dict['CLIMATE_ZONE_GROUP'] = [level, '==']
    if 'hot_summer-ii' in filter_dict:
        new_dict['HOT_SUMMER'] = [hot_summer_to_level[filter_dict['hot_summer-ii']], '==']
    if 'humidity-ii' in filter_dict:
        new_dict['HUMIDITY'] = [humidity_to_level[filter_dict['humidity-ii']], '==']
    if 'sunny-ii' in filter_dict:
        new_dict['SUNNY'] = [sunny_to_level[filter_dict['sunny-ii']], '==']
    if 'rainy-ii' in filter_dict:
        new_dict['RAINY'] = [rainy_to_level[filter_dict['rainy-ii']], '==']
    if 'snowy-ii' in filter_dict:
        new_dict['SNOWY'] = [1 if filter_dict['SNOWY'] == 'Yes' else 0, '==']
    return new_dict

@callback(Output('page-2-main', 'children'),
          Output('map', 'children'),
          Output('2s', 'data'),
          Output('zip-ii', 'value'),
          Output('distance', 'value'),
          Output('state-ii', 'value'),
          Output('tuition-ii', 'value'),
          Output('applfeeu-ii', 'value'),
          Output('exp-earnings-ii', 'value'),
          Output('select-cat-ii', 'value'),
          Output('climate-zone-ii', 'value'),
          Output('hot-summer-ii', 'value'),
          Output('humidity-ii', 'value'),
          Output('sunny-ii', 'value'),
          Output('rainy-ii', 'value'),
          Output('snowy-ii', 'value'),
          Input('page-2-title', 'children'),
          State('last-page', 'data'),
          State('new-page', 'data'),
          State('1s', 'data'),
          State('2s', 'data'),
          State('2s-filter', 'data'))
def page_2_load(unused, last_page, new_page, store1, store2, store2_filter):
    form = json.loads(store1)
    hovertemplate = '%{customdata[1]}<br>%{customdata[2]}, %{customdata[3]}'
    custom_data = ['UNITID', 'INSTNM', 'CITY', 'STABBR']
    filter_dict = dict(json.loads(store2_filter)) if store2_filter is not None else dict()
    if new_page == '/2/filter':
        print('page_2_load() - new_page= /2/filter')
        #filter_dict = dict(json.loads(store2_filter))
        local_df = pd.read_json(store2, typ='series')
        local_df, df = rec.filt(local_df, prepare_filters(filter_dict), create_user_info_dict(form))
        if df.shape[0] > 0:
            new_children = [fe.create_school_card(df.iloc[i, :]) for i in range(min(n, df.shape[0]))]
        else:
            new_children = []
        fig_map = px.scatter_mapbox(df.iloc[1:n, :], lat="LATITUDE", lon="LONGITUDE", custom_data=custom_data, color_discrete_sequence=["fuchsia"], zoom=3, height=300)
        fig_map.update_traces(hovertemplate=hovertemplate, marker_size=10)
        fig_map.update_layout(mapbox_style="white-bg", margin={"r":0, "t":0, "l":0, "b":0}, mapbox_layers=[
            {
                'below':'traces',
                'sourcetype':'raster',
                'sourceattribution':'United States Geological Survey',
                'source':['https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}']
            }])
        print(f'...returning from page_2_load... local_df sum: {np.sum(local_df)}')
        return new_children, dcc.Graph(id='map', figure=fig_map), local_df.to_json(), *filter_vals(filter_dict, reset=False)        
    elif new_page == '/2/filter0':
        print('page_2_load() - new_page= /2/filter0')
        local_df = pd.read_json(store2, typ='series')
        local_df, df = rec.filt(local_df, dict())
        if df.shape[0] > 0:
            new_children = [fe.create_school_card(df.iloc[i, :]) for i in range(min(n, df.shape[0]))]
        else:
            new_children = []
        fig_map = px.scatter_mapbox(df.iloc[1:n, :], lat="LATITUDE", lon="LONGITUDE", custom_data=custom_data, color_discrete_sequence=["fuchsia"], zoom=3, height=300)
        fig_map.update_traces(hovertemplate=hovertemplate, marker_size=10)
        fig_map.update_layout(mapbox_style="white-bg", margin={"r":0, "t":0, "l":0, "b":0}, mapbox_layers=[
            {
                'below':'traces',
                'sourcetype':'raster',
                'sourceattribution':'United States Geological Survey',
                'source':['https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}']
            }])
        print(f'...returning from page_2_load... local_df sum: {np.sum(local_df)}')
        return new_children, dcc.Graph(id='map', figure=fig_map), local_df.to_json(), *filter_vals(filter_dict, reset=True)
    elif last_page == '/1':  # if we came from page 1
        print('page_2_load() - last_page= /1')
        print(f'store1 = {store1}')
        form_dict = dict()
        fill_form(form, form_dict)
        df = rec.submit_form(form_dict, create_user_info_dict(form))
        local_df = pd.Series(data=True, index=df.index)
        new_children = [fe.create_school_card(df.iloc[i, :]) for i in range(n)]
        fig_map = px.scatter_mapbox(df.iloc[1:n, :], lat="LATITUDE", lon="LONGITUDE", custom_data=custom_data, color_discrete_sequence=["fuchsia"], zoom=3, height=300)
        fig_map.update_traces(hovertemplate=hovertemplate, marker_size=10)
        fig_map.update_layout(mapbox_style="white-bg", margin={"r":0, "t":0, "l":0, "b":0}, mapbox_layers=[
            {
                'below':'traces',
                'sourcetype':'raster',
                'sourceattribution':'United States Geological Survey',
                'source':['https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}']
            }])
        print(f'...returning from page_2_load... local_df sum: {np.sum(local_df)}')
        return new_children, dcc.Graph(id='map', figure=fig_map), local_df.to_json(), *filter_vals(filter_dict, reset=True)
    else:
        print('page_2_load() - else')
        local_df = pd.read_json(store2, typ='series')
        df = rec.get_data(local_df)
        if df.shape[0] > 0:
            new_children = [fe.create_school_card(df.iloc[i, :]) for i in range(min(n, df.shape[0]))]
        else:
            new_children = []
        fig_map = px.scatter_mapbox(df.iloc[1:n, :], lat="LATITUDE", lon="LONGITUDE", custom_data=custom_data, color_discrete_sequence=["fuchsia"], zoom=3, height=300)
        fig_map.update_traces(hovertemplate=hovertemplate, marker_size=10)
        fig_map.update_layout(mapbox_style="white-bg", margin={"r":0, "t":0, "l":0, "b":0}, mapbox_layers=[
            {
                'below':'traces',
                'sourcetype':'raster',
                'sourceattribution':'United States Geological Survey',
                'source':['https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}']
            }])
        print(f'...returning from page_2_load... local_df sum: {np.sum(local_df)}')
        return new_children, dcc.Graph(id='map', figure=fig_map), local_df.to_json(), *filter_vals(filter_dict, reset=False)


@callback(Output('2s-filter', 'data'),
          Input('zip-ii', 'value'),
          Input('distance', 'value'),
          Input('state-ii', 'value'),
          Input('tuition-ii', 'value'),
          Input('applfeeu-ii', 'value'),
          Input('exp-earnings-ii', 'value'),
          Input('select-cat-ii', 'value'),
          Input('climate-zone-ii', 'value'),
          Input('hot-summer-ii', 'value'),
          Input('humidity-ii', 'value'),
          Input('sunny-ii', 'value'),
          Input('rainy-ii', 'value'),
          Input('snowy-ii', 'value'))
def filter_input(zip_i, distance, state, tuition, applfeeu, earnings, select_cat, climate_zone,
                 hot_summer, humidity, sunny, rainy, snowy):
    filter_dict = {}
    if zip_i is not None:
        filter_dict['zip-ii'] = zip_i
    if distance is not None:
        filter_dict['distance'] = distance
    if state is not None:
        filter_dict['state-ii'] = state
    if tuition is not None:
        filter_dict['tuition-ii'] = tuition
    if applfeeu is not None:
        filter_dict['applfeeu-ii'] = applfeeu
    if earnings is not None:
        filter_dict['exp-earnings-ii'] = earnings
    if select_cat is not None:
        filter_dict['select-cat-ii'] = select_cat
    if climate_zone is not None:
        filter_dict['climate-zone-ii'] = climate_zone
    if hot_summer is not None:
        filter_dict['hot-summer-ii'] = hot_summer
    if humidity is not None:
        filter_dict['humidity-ii'] = humidity
    if snowy is not None:
        filter_dict['snowy-ii'] = snowy
    if sunny is not None:
        filter_dict['sunny-ii'] = sunny
    if rainy is not None:
        filter_dict['rainy-ii'] = rainy
    return json.dumps(filter_dict)
    

@callback(
    Output('url', 'pathname'),
    Input('map', 'clickData'), prevent_initial_call=True)
def display_click_data(clickData):
    if clickData is None:
        return '/2'
    else:
        return f'/college/{clickData["points"][0]["customdata"][0]}'


##############################  Page 3 ############################## 
@callback(Output('page-3-main', 'children'),
          Input('page-3-title', 'children'),
          State('new-page', 'data'),
          State('1s', 'data'))
def page_3_content(children, new_page, store1):
    print('page_3_content() - store1:')
    print(store1)
    form = json.loads(store1)
    if form['state-i'] is None:
        stabbr = 'IL'
    else:
        stabbr = state_to_stabbr[form['state-i']]
    unitid = int(new_page[9:])
    df = rec.get_data(pd.Series(data=[True], index=[unitid])).squeeze()
    return fe.create_college_info(df, stabbr)