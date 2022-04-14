from dash import html, dcc


majors = ["Agriculture, Agriculture Operations, And Related Sciences", "Natural Resources And Conservation", "Architecture And Related Services", "Area, Ethnic, Cultural, Gender, And Group Studies", "Communication, Journalism, And Related Programs", "Communications Technologies/Technicians And Support Services", "Computer And Information Sciences And Support Services", "Personal And Culinary Services", "Education", "Engineering", "Engineering Technologies And Engineering-Related Fields", "Foreign Languages, Literatures, And Linguistics",	"Family And Consumer Sciences/Human Sciences", "Legal Professions And Studies", "English Language And Literature/Letters", "Liberal Arts And Sciences, General Studies And Humanities", "Library Science", "Biological And Biomedical Sciences", "Mathematics And Statistics", "Military Technologies And Applied Sciences", "Multi/Interdisciplinary Studies",	"Parks, Recreation, Leisure, And Fitness Studies", "Philosophy And Religious Studies", "Theology And Religious Vocations", "Physical Sciences", "Science Technologies/Technicians", "Psychology", "Homeland Security, Law Enforcement, Firefighting And Related Protective Services", "Public Administration And Social Service Professions", "Social Sciences", "Construction Trades", "Mechanic And Repair Technologies/Technicians", "Precision Production", "Transportation And Materials Moving", "Visual And Performing Arts", "Health Professions And Related Programs", "Business, Management, Marketing, And Related Support Services", "History"]
climate_zones = {'Tropical (examples: Honolulu and Miami)':'A', 'Arid (examples: Pheonix and Denver)':'B', 'Temperate (examples: San Francisco and Atlanta)':'C', 'Continental (examples: Boston and Detroit)':'D'}

LOGO = "https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/1722948/college-student-clipart-md.png"

def create_slider(name):
    return dcc.Slider(1, 5, 1, id=f'{name}-imp-i', value=3,
        marks={1: 'Not Important', 3: 'Moderately Important', 5: 'Extremely Important'},
        className='slider'
    )


##############################  Page 1 ##############################
pageheader = html.Header(children=[
    html.Div(className='flex container', children=[
        html.Img(src=LOGO, height="90px"),
        html.A('College Recommendation Tool', href='/1'),
    ])
])

pageContent = html.Main(children=[
    html.Div(className='flexcols container', children=[
        # col 1
        html.Div(children=[
            html.H3('User Information'),
            html.Div(children=[
                html.Label('Select your desired major'),
                dcc.Dropdown(majors, id='major-i', optionHeight=80),
                html.Br(),
                
                html.Label('Enter your home zip code'),
                dcc.Input(placeholder='Zip Code', type='number', min=1, max=99950, value='', id='zip-i', debounce=True),
                html.Br(),

                html.Label('Enter your unweighted GPA'),
                dcc.Input(placeholder='X.XX', type='number', min=0, max=4, value = '', id='gpa-i', debounce =True),
                html.Br(),
            
                html.Label('Enter your SAT score'),
                dcc.Input(placeholder='XXXX', type='number', value = '', id='sat-i', debounce=True),
                html.Br(),
            
                html.Label('Enter your ACT score'),
                dcc.Input(placeholder='XXXX', type='number', value = '', id='act-i', debounce=True),
                html.Br(),
            ])
        ]),

        # col 2
        html.Div(children=[
            html.H3('Specific College Preferences'),
            html.Div(children=[
                html.Label('Select your desired tuition cost'),
                dcc.Slider(1, 5, 1, value=1, marks={1:'Inexpensive', 3:'Moderate', 5:'Expensive'}, id='cost-i', className='slider'),
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
                dcc.Slider(1, 5, 1, value=1, marks={1:'Small', 3:'Medium', 5:'Large'}, id='size-i', className='slider'),
                create_slider('size'),
                html.Br(),
                
                html.Label('Select your desired school environment'),
                dcc.Dropdown(['City', 'Suburb', 'Town', 'Rural'], id='environment-i'),
                create_slider('environment'),
                html.Hr()
            ])
        ]),

        # col 3
        html.Div(children=[
            html.H3('Additional Preferences'),
            html.Div(children=[
                html.P('How important is school selectivity to you?'),
                create_slider('selectivity'),
                html.P('How important is teaching quality to you?'),
                create_slider('teaching'),
                html.P('How important is projected earnings to you?'),
                create_slider('earnings')
            ])
        ])
    ])
])

page_1_layout = html.Div(children=[
    pageheader,
    pageContent,
    dcc.Link(html.Button('Submit'), href='/2')
])


##############################  Page 2 ##############################
page_2_layout = html.Div([
    html.H1('College Recommendation Tool'),
    html.H3('Recommendations'),
    html.Div(id='2c'),
    html.Div(id='map'),
    dcc.Link(html.Button('Back'), href='/1'),
])


##############################  Page 3 ##############################
page_3_layout = html.Div(id='page-3-layout')