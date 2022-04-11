from dash import Dash, dcc, html, Input, Output, callback, State
import json
import numpy as np
import pandas as pd


majors = ["Agriculture, Agriculture Operations, And Related Sciences", "Natural Resources And Conservation", "Architecture And Related Services", "Area, Ethnic, Cultural, Gender, And Group Studies", "Communication, Journalism, And Related Programs", "Communications Technologies/Technicians And Support Services", "Computer And Information Sciences And Support Services", "Personal And Culinary Services", "Education", "Engineering", "Engineering Technologies And Engineering-Related Fields", "Foreign Languages, Literatures, And Linguistics",	"Family And Consumer Sciences/Human Sciences", "Legal Professions And Studies", "English Language And Literature/Letters", "Liberal Arts And Sciences, General Studies And Humanities", "Library Science", "Biological And Biomedical Sciences", "Mathematics And Statistics", "Military Technologies And Applied Sciences", "Multi/Interdisciplinary Studies",	"Parks, Recreation, Leisure, And Fitness Studies", "Philosophy And Religious Studies", "Theology And Religious Vocations", "Physical Sciences", "Science Technologies/Technicians", "Psychology", "Homeland Security, Law Enforcement, Firefighting And Related Protective Services", "Public Administration And Social Service Professions", "Social Sciences", "Construction Trades", "Mechanic And Repair Technologies/Technicians", "Precision Production", "Transportation And Materials Moving", "Visual And Performing Arts", "Health Professions And Related Programs", "Business, Management, Marketing, And Related Support Services", "History"]
climate_zones = {"Tropical Rainforest":"Af", "Tropical Monsoon":"Am", "Tropical Savanna, Dry Summer":"As", "Tropical Savanna, Dry Winter":"Aw", "Arid Steppe, Hot":"BSh", "Arid Steppe, Cold":"BSk", "Arid Desert, Hot":"BWh", "Arid Desert, Cold":"BWk", "Temperate, No Dry Season, Hot Summer":"Cfa", "Temperate, No Dry Season, Warm Summer":"Cfb", "Temperate, Dry Summer, Hot Summer":"Csa", "Temperate, Dry Summer, Warm Summer":"Csb", "Continental, No Dry Season, Hot Summer":"Dfa", "Continental, No Dry Season, Warm Summer":"Dfb", "Continental, No Dry Season, Cold Summer":"Dfc", "Continental, Dry Winter, Hot Summer":"Dwa"}

# dummy functions to be replaced with Huy's final versions
df = pd.read_csv("../data/minimal.csv")
def startup():
    global df
    df = pd.read_csv("../data/minimal.csv")
    
def submit_form(form_data):
    a = int(np.random.random()*40)
    n = int(np.random.random()*5+1)
    return df.loc[a:(a+n), :]

def filter_colleges(df, filter_info):
    filter_info = json.loads(filter_info)
    return [True] * df.shape[0] if filter_info['filter-i'] else [True] + [False] * (df.shape[0]-1)

def similar_colleges(college_id, weights):
    i = [int(np.random.random()*100) for _ in range(3)]
    return df.loc[df.UNITID == college_id, :], df.iloc[i, :]
# end of dummy functions


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

@callback(Output('pc', 'children'),
          Input('new-page', 'data'))
def change_page(new_page):
    if new_page == '/1':
        return page_1_layout
    elif new_page == '/2':
        return page_2_layout
    elif new_page is None or new_page == '':
        return page_1_layout
    else:
        return page_3_layout


# Page 1
page_1_layout = html.Div(id='form', children=[
    html.H1('College Recommendation Tool'),
    html.H2('Page 1'),
    html.H3('User Information'),
    html.Label('Select your desired major'),
    dcc.Dropdown(majors, id='major-i'),
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
    dcc.Dropdown(id='climate-i', placeholder='Select your preferred climate type', options=list(climate_zones.keys())),
    dcc.Checklist(['Snowy Winters', 'Sunny Summers'], id='weather-types-i'),
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
])

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
    return f'{{"major":"{major_val}", "zip":{zip_val}, "gpa":{gpa_val}, "sat":{sat_val}, "act":{act_val}, "cost":{cost_val}, "cost-imp":{cost_imp_val}, "state":"{state_val}", "state-imp":{state_imp_val}, "climate":"{climate_val}", "weather-types":{weather_types_val}, "weather-imp":{weather_imp_val}, "size":{size_val}, "size-imp":{size_imp_val}, "environment":"{environment_val}", "environment-imp":{environment_imp_val}, "selectivity-imp":{selectivity_imp_val}, "teaching-imp":{teaching_imp_val}, "earnings-imp":{earnings_imp_val}}}'


# Page 2
page_2_layout = html.Div([
    html.H1('College Recommendation Tool'),
    html.H3('Recommendations'),
    html.Div(id='2c'),
    dcc.Link(html.Button('Back'), href='/1'),
])

@callback(Output('2c', 'children'),
          Output('2s', 'data'),
          Output('2s-minimal', 'data'),
          Input('2c', 'children'),
          State('last-page', 'data'),
          State('1s', 'data'),
          State('2s', 'data'),
          State('2s-minimal', 'data'))
def page_2_content(children, last_page, store1, store2, store2_m):
    if last_page == '/1':  # if we came from page 1
        df = submit_form(store1)
        return [dcc.Link(html.Div(id={'type':'listed-college', 'index':str(df.UNITID.iloc[i])}, n_clicks=0, children=[html.Hr(), html.Label(df.INSTNM.iloc[i]), html.Br(), html.P(f'{df.CITY.iloc[i]}, {df.STABBR.iloc[i]}')]), href=f'/college/{df.UNITID.iloc[i]}') for i in range(df.shape[0])], df.to_json(), df.iloc[0:min(10, df.shape[0]), :].to_json()
    else:
        df = pd.read_json(store2_m)
        return [dcc.Link(html.Div(id={'type':'listed-college', 'index':str(df.UNITID.iloc[i])}, n_clicks=0, children=[html.Hr(), html.Label(df.INSTNM.iloc[i]), html.Br(), html.P(f'{df.CITY.iloc[i]}, {df.STABBR.iloc[i]}')]), href=f'/college/{df.UNITID.iloc[i]}') for i in range(df.shape[0])], store2, store2_m


# page 3
page_3_layout = html.Div(id='page-3-layout')

@callback(Output('page-3-layout', 'children'),
          Input('page-3-layout', 'children'),
          State('new-page', 'data'))
def page_3_content(children, new_page):
    unitid = new_page[9:]
    (main, df) = similar_colleges(int(unitid), 'fake weights')
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

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='1s', storage_type='session'),
    dcc.Store(id='2s', storage_type='session'),
    dcc.Store(id='2s-minimal', storage_type='session'),
    dcc.Store(id='last-page', data='/1', storage_type='session'),
    dcc.Store(id='new-page', data='/1', storage_type='session'),
    html.Div(id='pc', children=page_1_layout)
])

if __name__ == '__main__':
    app.run_server(debug=True)