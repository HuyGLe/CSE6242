from dash import Dash, dcc, html, Input, Output
from plotly.express import data
import pandas as pd
import csv

#Load CSV file in 
df = pd.read_csv("test_data.csv")
#print(df)

### Degree Program Selection
app = Dash(__name__)
app.layout = html.Div([
    html.H1('College Recommendation Tool'),
    html.P(['Select major of study you are interested in.',
        html.Br()]),
    dcc.Dropdown(df.columns, id='majors-dropdown-1'),
    html.Div(id='majors-output-container-1'),
    html.Br(),
    html.Br(),
    html.Label('Please enter your home zip code:     '),
    dcc.Input(
        placeholder='Zip Code',
        type='text',
        value = '',
        id='zip-code-input',
        debounce =True
    ),
    html.Div(id='zip-code-container'),
    html.Br(),
    html.Br(),
    html.Label('Please enter your unweighted GPA:     '),
        dcc.Input(
        placeholder='X.XX',
        type='number',
        value = '',
        id='gpa-input',
        debounce =True
    ),
    html.Br(),
    html.Br(),
    html.Label('Please enter your SAT score:    '),
        dcc.Input(
        placeholder='XXXX',
        type='number',
        value = '',
        id='sat-input',
        debounce =True
    ),
    html.Br(),
    html.Br(),
    html.Label('Please enter your ACT score:    '),
        dcc.Input(
        placeholder='XXXX',
        type='number',
        value = '',
        id='act-input',
        debounce =True
    )

    
])

@app.callback(
    Output('majors-output-container-1', 'children'),
    Input('majors-dropdown-1', 'value')
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