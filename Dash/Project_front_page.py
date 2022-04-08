from dash import Dash, dcc, html, Input, Output, callback, State
import json
import numpy as np
import pandas as pd


DEGREES = ['Degree A', 'Degree B', 'Degree C']

def create_slider(name):
    return dcc.Slider(1, 5, 1, id=f'{name}-imp-i',
                      marks={1: 'Not Important', 3: 'Moderately Important', 5: 'Extremely Important'}
    )

def create_page_3_layout(unitid):
    college = df.loc[df.UNITID == int(unitid), :].squeeze()
    return html.Div([
        html.H1(str(college.INSTNM)),
        html.H2(f'{college.CITY}, {college.STABBR}'),
        html.P("More information and graphs"),
        html.P("Short list of similar schools"),
        dcc.Link(html.Button('Back'), href='/2')])

df = pd.read_csv("../data/minimal.csv")
app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='1s'),
    dcc.Store(id='2s'),
    dcc.Store(id='old_page', data='/1'),
    dcc.Store(id='temp_page', data='/1'),
    dcc.Store(id='new_page', data='/1'),
    html.Div(id='pc', children=(page_1_layout := html.Div(id='form', children=[
        html.H1('College Recommendation Tool'),
        html.H2('Page 1'),
        html.H3('User Information'),
        html.Label('Select your desired major'),
        dcc.Dropdown(DEGREES, id='major-i'),
        html.Br(),
        html.Label('Enter your home zip code'),
        dcc.Input(
            placeholder='Zip Code',
            type='number',
            min=1,
            max=99950,
            value = '',
            id='zip-i',
            debounce =True
        ),
        html.Br(),
        html.Label('Enter your unweighted GPA'),
        dcc.Input(
            placeholder='X.XX',
            type='number',
            min=0,
            max=4,
            value = '',
            id='gpa-i',
            debounce =True
        ),
        html.Br(),
        html.Label('Enter your SAT score'),
        dcc.Input(
            placeholder='XXXX',
            type='number',
            value = '',
            id='sat-i',
            debounce =True
        ),
        html.Br(),
        html.Label('Enter your ACT score'),
        dcc.Input(
        placeholder='XXXX',
            type='number',
            value = '',
            id='act-i',
            debounce =True
        ),
        html.Br(),
        html.Hr(),
        html.H3('Specific College Preferences'),
        html.Label('Select your desired tuition cost'),
        dcc.Slider(1, 5, 1, marks={1:'Inexpensive', 3:'Moderate', 5:'Expensive'}, id='cost-i'),
        create_slider('cost'),
        html.Br(),
        html.Label('Select your desired location'),
        dcc.Dropdown(id='state-i', placeholder='Select your preferred state', options=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']),
        create_slider('state'),
        html.Br(),
        html.Label('Select your desired weather'),
        dcc.Dropdown(id='climate-i', placeholder='Select your preferred climate type', options=['A', 'B', 'C', 'D', 'E', 'F']),
        dcc.Checklist(['Snowy winters', 'Sunny summers'], id='weather-types-i'),
        create_slider('weather'),
        html.Br(),
        html.Label('Select your desired school size'),
        dcc.Slider(1, 5, 1, marks={1:'Small', 3:'Medium', 5:'Large'}, id='size-i'),
        create_slider('size'),
        html.Br(),
        html.Label('Select your desired school environment'),
        dcc.Dropdown(['City', 'Suburb', 'Town', 'Rural'], id='environment-i'),
        create_slider('environment'),
        html.Hr(),
        html.H3('Additional Preferences'),
        html.P('How important is school selectivity to you?'),
        create_slider('selectivity'),
        html.P('How important is teaching quality to you?'),
        create_slider('teaching'),
        html.P('How important is projected earnings to you?'),
        create_slider('earnings'),
        dcc.Link(html.Button('Submit'), href='/2')
    ])))
])

@callback(Output('temp_page', 'data'),
          Input('url', 'pathname'),
          State('old_page', 'data'), suppress_callback_exceptions=True)
def update_temp(pathname, old_data):
    return old_data
    
@callback(Output('old_page', 'data'),
          Input('temp_page', 'data'),
          State('url', 'pathname'),
          State('old_page', 'data'),
          State('new_page', 'data'), suppress_callback_exceptions=True)
def update_old(temp_data, pathname, old_data, new_data):
    if pathname == new_data:
        return old_data
    else:
        return new_data
    
@callback(Output('new_page', 'data'),
          Input('old_page', 'data'),
          State('url', 'pathname'), suppress_callback_exceptions=True)
def update_new(old_data, pathname):
    if pathname == '/1':
        return '/1'
    elif pathname == '/2':
        return '/2'
    elif pathname[1:8] == 'college':
        return pathname[9:]
    else:
        return '/1'

@callback(Output('pc', 'children'),
          Input('new_page', 'data'), suppress_callback_exceptions=True)
def change_page(new_data):
    if new_data == '/1':
        return page_1_layout
    elif new_data == '/2':
        return page_2_layout
    elif new_data is None or new_data == '':
        return page_1_layout
    else:
        return create_page_3_layout(new_data)


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
    print(f'{{"major":"{major_val}", "zip":{zip_val}, "gpa":{gpa_val}, "sat":{sat_val}, "act":{act_val}, "cost":{cost_val}, "cost-imp":{cost_imp_val}, "state":"{state_val}", "state-imp":{state_imp_val}, "climate":"{climate_val}", "weather-types":{weather_types_val}, "weather-imp":{weather_imp_val}, "size":{size_val}, "size-imp":{size_imp_val}, "environment":"{environment_val}", "environment-imp":{environment_imp_val}, "selectivity-imp":{selectivity_imp_val}, "teaching-imp":{teaching_imp_val}, "earnings-imp":{earnings_imp_val}}}')
    return f'{{"major":"{major_val}", "zip":{zip_val}, "gpa":{gpa_val}, "sat":{sat_val}, "act":{act_val}, "cost":{cost_val}, "cost-imp":{cost_imp_val}, "state":"{state_val}", "state-imp":{state_imp_val}, "climate":"{climate_val}", "weather-types":{weather_types_val}, "weather-imp":{weather_imp_val}, "size":{size_val}, "size-imp":{size_imp_val}, "environment":"{environment_val}", "environment-imp":{environment_imp_val}, "selectivity-imp":{selectivity_imp_val}, "teaching-imp":{teaching_imp_val}, "earnings-imp":{earnings_imp_val}}}'


# Page 2
page_2_layout = html.Div([
    html.H1('College Recommendation Tool'),
    html.H3('Recommendations'),
    html.Div(id='2c'),
    dcc.Link(html.Button('Back'), href='/1'),
])

@callback(Output('2c', 'children'),
          Input('2c', 'children'),
          State('old_page', 'data'),
          State('1s', 'data'),
          State('2s', 'data'))
def page_2_content(children, old_page_data, store1, store2):
    if old_page_data == '/1':  #if we came from page 1
        n = int(np.random.random()*5+1)
        return [dcc.Link(html.Div(id={'type':'listed-college', 'index':str(df.UNITID[i])}, n_clicks=0, children=[html.Hr(), html.Label(df.INSTNM[i]), html.Br(), html.P(f'{df.CITY[i]}, {df.STABBR[i]}')]), href=f'/college/{df.UNITID[i]}') for i in range(n)]
    elif old_page_data == '/2':
        return children
    else:
        ## TODO: make this json into actual objects
        return store2
        
@callback(Output('2s', 'data'),
          Input('2c', 'children'))
def update_2s(children):
    print(json.dumps(children))
    return json.dumps(children)

if __name__ == '__main__':
    app.run_server(debug=True)