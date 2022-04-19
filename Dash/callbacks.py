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
          Input('exp-earnings-imp', 'value'), prevent_initial_call=True)
def page_1_input(major, zipcode, gpa, sat, act, state, state_imp, ugds, ugds_imp, locale_first, locale_first_imp,
                 climate_zone, hot_summer, humidity, sunny, rainy, snowy, weather_imp, tuition_imp, select_imp,
                 teach_qual_imp, exp_earnings_imp):
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
    form['locale-first'] = locale_first
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
    return json.dumps(form)

##############################  Page 2 ##############################
def filter_vals(filter_dict, reset):
    if reset == True:
        zip_ii = None
        distance = None
        state_ii = None
    else:
        zip_ii = filter_dict['ZIP'][0] if 'ZIP' in filter_dict else None
        distance = f'{filter_dict["DISTANCE"][0]} miles' if 'DISTANCE' in filter_dict else None
        state_ii =  stabbr_to_state[filter_dict['STABBR'][0]] if 'STABBR' in filter_dict else None
    return [zip_ii, distance, state_ii]

def create_user_info_dict(form):
    info = dict()
    if 'major-i' in form:
        info['major'] = form['major-i']
    if 'gpa-i' in form:
        info['gpa'] = form['gpa-i']
    if 'zip-i' in form:
        info['zip'] = form['zip-i']
    if 'sat-i' in form:
        info['sat'] = form['sat-i']
    if 'act-i' in form:
        info['act'] = form['act-i']
    return info

@callback(Output('page-2-main', 'children'),
          Output('map', 'children'),
          Output('2s', 'data'),
          Output('zip-ii', 'value'),
          Output('distance', 'value'),
          Output('state-ii', 'value'),
          Input('page-2-title', 'children'),
          State('last-page', 'data'),
          State('new-page', 'data'),
          State('1s', 'data'),
          State('2s', 'data'),
          State('2s-filter', 'data'))
def page_2_load(unused, last_page, new_page, store1, store2, store2_filter):
    hovertemplate = '%{customdata[1]}<br>%{customdata[2]}, %{customdata[3]}'
    custom_data = ['UNITID', 'INSTNM', 'CITY', 'STABBR']
    filter_dict = dict(json.loads(store2_filter))
    if new_page == '/2/filter':
        print('page_2_load() - new_page= /2/filter')
        local_df = pd.read_json(store2, typ='series')
        local_df, df = rec.filt(local_df, filter_dict)
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
        form = json.loads(store1)
        form_dict = dict()
        misc = dict()
        if 'major-i' in form:
            form_dict[f'CIP{major_to_num[form["major-i"]]}BACHL'] = [1, 5]
        if 'state-i' in form:
            form_dict[f'STABBR.{state_to_stabbr[form["state-i"]]}'] = [1, int(form['state-imp'])]
            misc['state'] = [state_to_stabbr[form["state-i"]], int(form['state-imp'])]
        form_dict['UGDS'] = [int(form['ugds-i']), int(form['ugds-imp'])]
        if 'locale-first-i' in form:
            form_dict[f'LOCALE_FIRST.{locale_first_to_num[form["locale_first"]]}'] = [1 , int(form['locale_first-imp'])]
        if 'climate-zone-i' in form: 
            form_dict[f'CLIMATE_ZONE_GROUP.{climate_zone_groups[form["climate-zone-i"]]}'] = [1, int(form['weather-imp'])]
        if 'hot-summer-i' in form:
            form_dict['HOT_SUMMER'] = [hot_summer_to_level[form['hot-summer-i']], int(form["weather-imp"])]
        if 'humidity-i' in form:
            form_dict['HUMIDITY'] = [humidity_to_level[form['humidity-i']], int(form["weather-imp"])]
        if 'sunny-i' in form:
            form_dict['SUNNY'] = [sunny_to_level[form['sunny-i']], int(form["weather-imp"])]
        if 'rainy-i' in form:
            form_dict['RAINY'] = [rainy_to_level[form['rainy-i']], int(form["weather-imp"])]
        form_dict['SNOWY'] = [1 if len(form['snowy-i'])==1 else 0, form["weather-imp"]]
        form_dict['TUITION'] = [None, int(form['tuition-imp'])]
        form_dict['SELECT'] = [None, int(form['select-imp'])]
        form_dict['TEACH_QUAL'] = [None, int(form['teach-qual-imp'])]
        form_dict['EXP_EARNINGS'] = [None, int(form['exp-earnings-imp'])]
        df = rec.submit_form(form_dict, create_user_info_dict(form), misc)
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
          Input('state-ii', 'value'))
def filter_input(zip_i, distance, state):
    filter_dict = {}
    if zip_i is not None:
        filter_dict['ZIP'] = [zip_i, '*']
    if distance is not None:
        filter_dict['DISTANCE'] = [int(distance.split(' ')[0]), '*']
    if state is not None:
        filter_dict['STABBR'] = [state_to_stabbr[state], '==']
    print('filter_input(): state is ' + ('not' if state is not None else '') + 'None; setting state-ii to ' + json.dumps(filter_dict))
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
    stabbr = state_to_stabbr[form['state-i']]
    unitid = int(new_page[9:])
    df = rec.get_data(pd.Series(data=[True], index=[unitid])).squeeze()
    return fe.create_college_info(df, stabbr)