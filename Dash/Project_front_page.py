from dash import Dash, dcc, html, Input, Output, State
from plotly.express import data
import pandas as pd
import csv
import json


#Load CSV file in 
df = pd.read_csv("../data/final.csv")

### Degree Program Selection
app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='page-number-store', data='1', storage_type='session'),
    dcc.Store(id='page-1-store', storage_type='session', data="default"),
    dcc.Store(id='college-results-store', storage_type='session'),
    dcc.Store(id='second-page-filters-store', storage_type='session'),
    html.Div(id='page-content')
])

page_1_layout = html.Div([
    html.H1('College Recommendation Tool'),
    html.H3('User Information'),
    html.P(['Select major of study you are interested in.',
        html.Br()]),
    dcc.Dropdown(df.columns, id='major-input'),
    html.Div(id='majors-output-container-1'),
    html.Br(),
    html.Br(),
    html.Label('Please enter your home zip code:'),
    dcc.Input(
        placeholder='Zip Code',
        type='number',
        min=1,
        max=99950,
        value = '',
        id='zip-code-input',
        debounce =True
    ),
    html.Br(),
    html.Br(),
    html.Label('Please enter your unweighted GPA:'),
        dcc.Input(
        placeholder='X.XX',
        type='number',
        min=0,
        max=4,
        value = '',
        id='gpa-input',
        debounce =True
    ),
    html.Br(),
    html.Br(),
    html.Label('Please enter your SAT score:'),
        dcc.Input(
        placeholder='XXXX',
        type='number',
        value = '',
        id='sat-input',
        debounce =True
    ),
    html.Br(),
    html.Br(),
    html.Label('Please enter your ACT score:'),
        dcc.Input(
        placeholder='XXXX',
        type='number',
        value = '',
        id='act-input',
        debounce =True
    ),
    html.Hr(),
    html.H3('Specific College Preferences'),
    html.P('Location'),
    dcc.Dropdown(id='preferred-state-input', placeholder='Select your preferred state', options=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']),
    dcc.Slider(1, 5, 1, id='preferred-state-importance',
        marks={
            1: 'Not Important',
            3: 'Moderately Important',
            5: 'Extremely Important'
        }
    ),
    html.Br(),
    html.P('Weather'),
    dcc.Dropdown(id='preferred-climate-input', placeholder='Select your preferred climate type', options=['A', 'B', 'C', 'D', 'E', 'F']),
    dcc.Checklist(['Snowy winters', 'Sunny summers'], id='preferred-weather-types-input'),
    dcc.Slider(1, 5, 1, id='preferred-weather-importance',
        marks={
            1: 'Not Important',
            3: 'Moderately Important',
            5: 'Extremely Important'
        }
    ),
    html.Hr(),
    html.H3('Additional Preferences'),
    html.P('How important is teaching quality to you?'),
    dcc.Slider(1, 5, 1, id='teaching-quality-importance',
        marks={
            1: 'Not Important',
            3: 'Moderately Important',
            5: 'Extremely Important'
        }
    ),
    dcc.Link(html.Button('Submit', id='page-1-button', n_clicks=0), href='/page-2', id='page-1-link')
])

page_2_layout = html.Div([
    html.H1('Recommendations'),
    html.H3('A list of schools will be here', id='page-2-h3'),
    html.P('This is default text for testing purposes', id='test-text'),
    dcc.Link(html.Button('Back', id='page-2-button', n_clicks=0), href='/page-1')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page-2':
        return page_2_layout
    else:
        return page_1_layout
    
@app.callback(Output('first-page-store', 'data'),
              Input('page-1-link', 'n_clicks'),
              State('zip-code-input', 'value'))
def page_1_button(n_clicks, zip_value):
    return f'the zip code is {zip_value}'

@app.callback(Output('test-text', 'children'),
              Input('page-2-h3', 'children'),
              State('page-1-store', 'data'))
def page_2_load(children, store_data):
    return f'The zip code from the previous page was {store_data}'

@app.callback(
    Output('majors-output-container-1', 'children'),
    Input('majors-input', 'value')
)
def update_output(value):
    return f'You have selected the {value} degree program '
    
    
#@app.callback(
#    Output('zip-code-container', 'children'),
#    Input('zip-code-input','value')
#)

#ALLOWED_TYPES = (
#    "text", "number", "password", "email", "search",
#    "tel", "url", "range", "hidden",
#)


#app.layout = html.Div(
#    [
#        dcc.Input(
#            id="input_{}".format(_),
#            type=_,
#            placeholder="input type {}".format(_),
#        )
#        for _ in ALLOWED_TYPES
#    ]
#    + [html.Div(id="out-all-types")]
#)


#@app.callback(
#    Output("out-all-types", "children"),
#    [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
#)
#def cb_render(*vals):
#    return " | ".join((str(val) for val in vals if val))


if __name__ == '__main__':
    app.run_server(debug=True)