import dash
from dash import Dash, dcc, html, Input, Output, callback, State
import json
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import dash_daq as daq

majors = ["Agriculture, Agriculture Operations, And Related Sciences", "Natural Resources And Conservation", "Architecture And Related Services", "Area, Ethnic, Cultural, Gender, And Group Studies", "Communication, Journalism, And Related Programs", "Communications Technologies/Technicians And Support Services", "Computer And Information Sciences And Support Services", "Personal And Culinary Services", "Education", "Engineering", "Engineering Technologies And Engineering-Related Fields", "Foreign Languages, Literatures, And Linguistics",	"Family And Consumer Sciences/Human Sciences", "Legal Professions And Studies", "English Language And Literature/Letters", "Liberal Arts And Sciences, General Studies And Humanities", "Library Science", "Biological And Biomedical Sciences", "Mathematics And Statistics", "Military Technologies And Applied Sciences", "Multi/Interdisciplinary Studies",	"Parks, Recreation, Leisure, And Fitness Studies", "Philosophy And Religious Studies", "Theology And Religious Vocations", "Physical Sciences", "Science Technologies/Technicians", "Psychology", "Homeland Security, Law Enforcement, Firefighting And Related Protective Services", "Public Administration And Social Service Professions", "Social Sciences", "Construction Trades", "Mechanic And Repair Technologies/Technicians", "Precision Production", "Transportation And Materials Moving", "Visual And Performing Arts", "Health Professions And Related Programs", "Business, Management, Marketing, And Related Support Services", "History"]
climate_zones = {"Tropical Rainforest":"Af", "Tropical Monsoon":"Am", "Tropical Savanna, Dry Summer":"As", "Tropical Savanna, Dry Winter":"Aw", "Arid Steppe, Hot":"BSh", "Arid Steppe, Cold":"BSk", "Arid Desert, Hot":"BWh", "Arid Desert, Cold":"BWk", "Temperate, No Dry Season, Hot Summer":"Cfa", "Temperate, No Dry Season, Warm Summer":"Cfb", "Temperate, Dry Summer, Hot Summer":"Csa", "Temperate, Dry Summer, Warm Summer":"Csb", "Continental, No Dry Season, Hot Summer":"Dfa", "Continental, No Dry Season, Warm Summer":"Dfb", "Continental, No Dry Season, Cold Summer":"Dfc", "Continental, Dry Winter, Hot Summer":"Dwa"}

app = dash.Dash(
    __name__,
    external_stylesheets=['style.css'],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
)

STUD_LOGO = "https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/1722948/college-student-clipart-md.png"
COLLEGE_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Georgia_Tech_seal.svg/225px-Georgia_Tech_seal.svg.png"

pageheader = html.Header(children=[
    html.Div(className='flex container', children=[
        html.Img(src=STUD_LOGO, height="90px"),
        html.A('College Recommendation Tool', href='/1'),
        html.Br()
    ]),
    html.Div(className='flex_container', children=[
        ###INSERT GRAPHIC USED FOR SCHOOL HERE,
        html.Br(),
        html.Img(src=COLLEGE_LOGO, height="90px"),
        html.A("Georgia Tech", href='/1'),
    ])
])

def create_slider(name):
    return dcc.Slider(1, 5, 1, id=f'{name}-imp-i',
        marks={1: 'Not Important', 3: 'Moderately Important', 5: 'Extremely Important'},
        className='slider'
    )

def create_gauge(name):
    return daq.Gauge(
        color={"gradient":True,"ranges":{"red":[0,6],"yellow":[6,8],"green":[8,10]}},
        value=2,
        max=10,
        min=0,
        scale= {
                "custom": {
                    0: {"label": "Unlikely"},
                    2.5: {"label": "Not Very Likely"},
                    5.0: {"label":"Possible"},
                    7.5: {"label": "Likely"},
                    10: {"label": "Very Likely"},
                        },
                },
    )
    

pageContent = html.Main(children=[
    html.Div(className='flexcols container', children=[
        # col 1
        html.Div(children=[
            html.H3('College Overview'),
            html.Div(children=[
                html.Label('Student Population'),
                #Callback to Student Population Field
                html.P('34,000'),
                html.Br(),
                
                html.Label('Location'),
                #Callback to Location Field
                html.P("Atlanta"),
                html.Br(),

                html.Label('Website'),
                #Callback to college website Field
                html.P("www.gatech.edu"),
                html.Br(),
            
                html.Label('School Type'),
                #Callback to school type field
                html.P("Public"),
                html.Br(),
            
                html.Label('Setting'),
                #Callback to school setting field
                html.P("Large City"),
                html.Br(),

                html.Label('Demographics'),
                #Insert Demographics charts below for Ethnicity, M/F ratio, Avg Income
                html.P("Place the demographic charts below here"),
                html.Br(),
            ])
        ]),

        # col 2
        html.Div(children=[
            html.H3('Academic & Acceptance Info'),
            html.Div(children=[
                html.Label('Chances of being accepted'),
                create_gauge('accept_gauge-1'),
                html.Br(),

                html.Label("Percentage of Applications Accepted"),
                #Insert applications accepted as percentage
                html.P("21.3%"),
                html.Br(),

                html.Label("Average SAT scores accepted"),
                #Insert applications accepted as percentage
                html.P("1400"),
                html.Br(),

                html.Label("Average ACT score accepted"),
                #Insert applications accepted as percentage
                html.P("26"),
                html.Br(),

                html.Label("Average unweighted GPA accepted"),
                #Insert applications accepted as percentage
                html.P("3.95"),
                html.Br(),
            ])
        ]),

        # col 3
        html.Div(children=[
            html.H3('Cost and Expected Return Information'),
            html.Div(children=[
                html.Label("Cost Information"),
                #Insert cost information chart here
                html.P("Place the cost information charts here"),
                html.Br(),

                html.Label("Average Salary After 10 Years"),
                #Insert average salary after 10 information
                html.P("10 year average salary info goes here"),
                html.Br(),
            ])
        ])
    ])
])

app.layout = html.Div(children=[
    pageheader,
    pageContent
])

if __name__ == '__main__':
    app.run_server(debug=True)