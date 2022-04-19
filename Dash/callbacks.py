import json
import pandas as pd
from dash import Input, Output, State, callback, html, dcc
import plotly.express as px
import sys
sys.path.append('./scripts')
import recommendation_engine as rec
import front_end as fe

state_to_stabbr = dict(zip(['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'], ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']))
climate_zone_groups = {'Tropical (examples: Honolulu and Miami)':'A', 'Arid (examples: Pheonix and Denver)':'B', 'Temperate (examples: San Francisco and Atlanta)':'C', 'Continental (examples: Boston and Detroit)':'D'}
weather_type_to_col = {}

                           # Global
@callback(Output('new-page', 'data'),
          Output('last-page', 'data'),
          Input('url', 'pathname'),
          State('new-page', 'data'),
          State('last-page', 'data'))
def url_update(pathname, new_page, last_page):
    if pathname == '/1' or pathname == '/2' or pathname[1:8] == 'college':
        return pathname, new_page
    else:
        return '/1', '/1'
    
    
# Page 1
@callback(Output('1s', 'data'),
          Input('major-i', 'value'),
          Input('zip-i', 'value'),
          Input('gpa-i', 'value'),
          Input('sat-i', 'value'),
          Input('act-i', 'value'),
          Input('cost-i', 'value'),
          Input('cost-imp-i', 'value'),
          Input('state-i', 'value'),
          Input('state-imp-i', 'value'),
          Input('climate-i', 'value'),
          Input('weather-types-i', 'value'),
          Input('weather-imp-i', 'value'),
          Input('size-i', 'value'),
          Input('size-imp-i', 'value'),
          Input('environment-i', 'value'),
          Input('environment-imp-i', 'value'),
          Input('selectivity-imp-i', 'value'),
          Input('teaching-imp-i', 'value'),
          Input('earnings-imp-i', 'value'), prevent_initial_call=True)
def page_1_input(major_val, zip_val, gpa_val, sat_val, act_val, cost_val, cost_imp_val,
                state_val, state_imp_val, climate_val, weather_types_val, weather_imp_val,
                size_val, size_imp_val, environment_val, environment_imp_val,
                selectivity_imp_val, teaching_imp_val, earnings_imp_val):
    return f'{{"major":"{major_val}", "zip":"{zip_val}", "gpa":"{gpa_val}", "sat":"{sat_val}", "act":"{act_val}", "cost":"{cost_val}", "cost-imp":"{cost_imp_val}", "state":"{state_val}", "state-imp":"{state_imp_val}", "climate":"{climate_val}", "weather-types":"{weather_types_val}", "weather-imp":"{weather_imp_val}", "size":"{size_val}", "size-imp":"{size_imp_val}", "environment":"{environment_val}", "environment-imp":"{environment_imp_val}", "selectivity-imp":"{selectivity_imp_val}", "teaching-imp":"{teaching_imp_val}", "earnings-imp":"{earnings_imp_val}"}}'


# Page 2
@callback(Output('page-2-main', 'children'),
          Output('map', 'children'),
          Output('2s', 'data'),
          Input('page-2-title', 'children'),
          State('last-page', 'data'),
          State('1s', 'data'),
          State('2s', 'data'))
def page_2_load(unused, last_page, store1, store2):
    print('****************** PAGE_2_LOAD *****************')
    n = 12 # number of schools listed
    hovertemplate = '%{customdata[1]}<br>%{customdata[2]}, %{customdata[3]}'
    custom_data = ['UNITID', 'INSTNM', 'CITY', 'STABBR']
    if last_page == '/1':  # if we came from page 1
        form = json.loads(store1)
        form_dict = dict()
        form_dict[f'STABBR.{state_to_stabbr[form["state"]]}'] = [1, int(form['state-imp'])]
        form_dict[f'CLIMATE_ZONE_GROUP.{climate_zone_groups[form["climate"]]}'] = [1, int(form['weather-imp'])]
        #if form['weather-types'] is not None:
        #    for checked in form['weather-types']:
        #        form_dict[weather_type_to_col[checked]] = [1, int(form['weather-imp'])]
        form_dict['UGDS'] = [int(form['size']), int(form['size-imp'])]
        form_dict['TUITION'] = [int(form['cost']), int(form['cost-imp'])]
        form_dict['SELECT'] = [None, int(form['selectivity-imp'])]
        form_dict['TEACH_QUAL'] = [None, int(form['teaching-imp'])]
        df = rec.submit_form(form_dict, int(form['zip']))
        local_df = pd.Series(data=True, index=df.index)
        print(df.iloc[0:4, 0])
        print('xxx')
        print(local_df.iloc[0:4])
        print('01')
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
        return new_children, dcc.Graph(id='map', figure=fig_map), local_df.to_json()
    else:
        local_df = pd.read_json(store2, typ='series')
        print('yyy')
        print(local_df.iloc[0:4])
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
        return new_children, dcc.Graph(id='map', figure=fig_map), store2


@callback(
    Output('url', 'pathname'),
    Input('map', 'clickData'), prevent_initial_call=True)
def display_click_data(clickData):
    if clickData is None:
        return '/2'
    else:
        return f'/college/{clickData["points"][0]["customdata"][0]}'


# Page 3
@callback(Output('page-3-main', 'children'),
          Input('page-3-title', 'children'),
          State('new-page', 'data'),
          State('1s', 'data'))
def page_3_content(children, new_page, store1):
    form = json.loads(store1)
    stabbr = state_to_stabbr[form['state']]
    unitid = int(new_page[9:])
    df = rec.get_data(pd.Series(data=[True], index=[unitid])).squeeze()
    return fe.create_college_info(df, stabbr)