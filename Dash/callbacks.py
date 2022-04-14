import json
import pandas as pd
from dash import Input, Output, State, callback, html, dcc
import plotly.express as px
import sys
sys.path.append('./scripts')
import recommendation_engine as rec


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
@callback(Output('2c', 'children'),
          Output('map', 'children'),
          Output('2s', 'data'),
          Input('2c', 'children'),
          State('last-page', 'data'),
          State('1s', 'data'),
          State('2s', 'data'),)
def page_2_content(children, last_page, store1, store2):
    print('page_2_content')
    n = 12 # number of schools listed
    hovertemplate = '%{customdata[1]}<br>%{customdata[2]}, %{customdata[3]}'
    custom_data = ['UNITID', 'INSTNM', 'CITY', 'STABBR']
    if last_page == '/1':  # if we came from page 1
        form = json.loads(store1)
        form_dict = dict()
        form_dict['UGDS'] = [int(form['size']), int(form['size-imp'])]
        form_dict['TUITION'] = [int(form['cost']), int(form['cost-imp'])]
        form_dict['TEACH_QUAL'] = [None, int(form['teaching-imp'])]
        form_dict['SELECT'] = [None, int(form['selectivity-imp'])]
        df = rec.submit_form(form_dict, int(form['zip']))
        local_df = pd.Series(data=True, index=df.index)
        fig_map = px.scatter_mapbox(df.iloc[1:n, :], lat="LATITUDE", lon="LONGITUDE", custom_data=custom_data, color_discrete_sequence=["fuchsia"], zoom=3, height=300)
        fig_map.update_traces(hovertemplate=hovertemplate, marker_size=10)
        fig_map.update_layout(mapbox_style="white-bg", margin={"r":0, "t":0, "l":0, "b":0}, mapbox_layers=[
            {
                'below':'traces',
                'sourcetype':'raster',
                'sourceattribution':'United States Geological Survey',
                'source':['https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}']
            }])
        return [dcc.Link(html.Div(id={'type':'listed-college', 'index':str(df.UNITID.iloc[i])}, n_clicks=0, children=[html.Hr(), html.Label(df.INSTNM.iloc[i]), html.Br(), html.P(f'{df.CITY.iloc[i]}, {df.STABBR.iloc[i]}')]), href=f'/college/{df.UNITID.iloc[i]}') for i in range(min(10, df.shape[0]))], dcc.Graph(id='map', figure=fig_map), local_df.to_json()
    else:
        local_df = pd.read_json(store2)
        df = rec.get_data(local_df)
        df = df.loc[local_df, :]
        if df.shape[0] > 0:
            df = df.iloc[0:max(n, df.shape[0]), :]
        fig_map = px.scatter_mapbox(df.iloc[1:n, :], lat="LATITUDE", lon="LONGITUDE", custom_data=custom_data, color_discrete_sequence=["fuchsia"], zoom=3, height=300)
        fig_map.update_traces(hovertemplate=hovertemplate, marker_size=10)
        fig_map.update_layout(mapbox_style="white-bg", margin={"r":0, "t":0, "l":0, "b":0}, mapbox_layers=[
            {
                'below':'traces',
                'sourcetype':'raster',
                'sourceattribution':'United States Geological Survey',
                'source':['https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}']
            }])
        return [dcc.Link(html.Div(id={'type':'listed-college', 'index':str(df.UNITID.iloc[i])}, n_clicks=0, children=[html.Hr(), html.Label(df.INSTNM.iloc[i]), html.Br(), html.P(f'{df.CITY.iloc[i]}, {df.STABBR.iloc[i]}')]), href=f'/college/{df.UNITID.iloc[i]}') for i in range(min(10, df.shape[0]))], dcc.Graph(id='map', figure=fig_map), store2

@callback(
    Output('url', 'pathname'),
    Input('map', 'clickData'), prevent_initial_call=True)
def display_click_data(clickData):
    if clickData is None:
        return '/2'
    else:
        return f'/college/{clickData["points"][0]["customdata"][0]}'


# Page 3
@callback(Output('page-3-layout', 'children'),
          Input('page-3-layout', 'children'),
          State('new-page', 'data'))
def page_3_content(children, new_page):
    unitid = new_page[9:]
    (main, df) = rec.similar_colleges(int(unitid), 'fake weights')
    return html.Div([
        html.H1(main.INSTNM.iloc[0]),
        html.H3(f'{main.CITY.iloc[0]}, {main.STABBR.iloc[0]}'),
        html.P(f'Detailed information about {main.INSTNM.iloc[0]}, including graphs'),
        html.Hr(),
        html.H2('Similar Colleges:'),
        html.Div([
            dcc.Link(html.H4(f'{df.INSTNM.iloc[i]} : {df.CITY.iloc[i]}, {df.STABBR.iloc[i]}'), href=f'/college/{df.UNITID.iloc[i]}') 
            for i in range(3)
        ]),
        dcc.Link(html.Button('Back'), href='/2')
    ])