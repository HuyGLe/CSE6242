from dash import html, dcc
import sys
sys.path.append('./scripts')
import recommendation_engine as rec
import dash_daq as daq


majors = ["Agriculture, Agriculture Operations, And Related Sciences", "Natural Resources And Conservation", "Architecture And Related Services", "Area, Ethnic, Cultural, Gender, And Group Studies", "Communication, Journalism, And Related Programs", "Communications Technologies/Technicians And Support Services", "Computer And Information Sciences And Support Services", "Personal And Culinary Services", "Education", "Engineering", "Engineering Technologies And Engineering-Related Fields", "Foreign Languages, Literatures, And Linguistics",	"Family And Consumer Sciences/Human Sciences", "Legal Professions And Studies", "English Language And Literature/Letters", "Liberal Arts And Sciences, General Studies And Humanities", "Library Science", "Biological And Biomedical Sciences", "Mathematics And Statistics", "Military Technologies And Applied Sciences", "Multi/Interdisciplinary Studies",	"Parks, Recreation, Leisure, And Fitness Studies", "Philosophy And Religious Studies", "Theology And Religious Vocations", "Physical Sciences", "Science Technologies/Technicians", "Psychology", "Homeland Security, Law Enforcement, Firefighting And Related Protective Services", "Public Administration And Social Service Professions", "Social Sciences", "Construction Trades", "Mechanic And Repair Technologies/Technicians", "Precision Production", "Transportation And Materials Moving", "Visual And Performing Arts", "Health Professions And Related Programs", "Business, Management, Marketing, And Related Support Services", "History"]
climate_zone_groups = {'Tropical (e.g. Miami)':'A', 'Arid (e.g. Phoenix)':'B', 'Temperate (e.g. San Francisco)':'C', 'Continental (e.g. Boston)':'D'}
climate_zone_groups_inv = {v:k for k,v in climate_zone_groups.items()}
hot_summer_to_level = {'Cool':1, 'Moderate':2, 'Warm':3, 'Hot':4}
level_to_hot_summer = {v:k for k,v in hot_summer_to_level.items()}
humidity_to_level = {'Dry':1, 'Moderate':2, 'Humid':3, 'Very Humid':4}
level_to_humidity = {v:k for k,v in humidity_to_level.items()}
sunny_to_level = {'Cloudy':1, 'Some Sun':2, 'Very Sunny':3}
level_to_sunny = {v:k for k,v in sunny_to_level.items()}
rainy_to_level = {'Desert':1, 'Low':2, 'Moderate':3, 'Rainy':4}
level_to_rainy = {v:k for k,v in rainy_to_level.items()}
locale = {
    11:'Large City',
    12:'Midsize City',
    13:'Small City',
    21:'Large Suburb',
    22:'Midsize Suburb',
    23:'Small Suburb',
    31:'Town Near A City',
    32:'Town',
    33:'Remote Town',
    41:'Rural Area Near A City',
    42:'Rural Area',
    43:'Remote Rural Area'
}

LOGO = "https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/1722948/college-student-clipart-md.png"

def create_slider(name):
    return dcc.Slider(1, 5, 1, id=f'{name}-imp', value=3,
        marks={1: 'Not Important', 3: 'Moderately Important', 5: 'Extremely Important'},
        className='slider'
    )

def create_gauge(rank_diff):
    return daq.Gauge(
        color={"gradient":True,"ranges":{"red":[-7,-2.33],"yellow":[-2.33,2.33],"green":[2.33,7]}},
        max=7,
        min=-7,
        value=rank_diff,
        scale= {
                "custom": {
                    -7: {"label": "Unlikely", 'style':{'font-size':'10px'}},
                    -2.33: {"label": "Not Very Likely",'style':{'font-size':'10px'}},
                    0: {"label":"Possible", 'style':{'font-size':'10px'}},
                    2.33: {"label": "Likely", 'style':{'font-size':'10px'}},
                    7: {"label": "Very Likely", 'style':{'font-size':'10px'}},
                        },
                },
    )

def create_school_card(info):
    card = html.A(className='card summary-card', href=f'/college/{info.UNITID}', children=[
        html.Picture(className='thumbnail', children=[
            ###Get school picture
            html.Img(className='category__01', src=f'/assets/images/colleges/{info.IMAGE}')
        ]),
        html.Div(className='card-content', children=[
            ###Get school long name
            html.H4(f'{info.INSTNM}', className='college-name'),
            html.H5(f'{info.CITY}, {info.STABBR}', className='college-city'),

            html.Div(className='key-val', children=[
                html.Span('Required GPA', className='key'),
                html.Span(f'{round(info.GPA_BOTTOM_TEN_PERCENT, 1)}', className='val'),
            ]),
            
            html.Div(className='key-val', children=[
                html.Span('Average SAT Score', className='key'),
                html.Span(f'{int(info.SAT_AVG)}', className='val'),
            ]),
            
            html.Div(className='key-val', children=[
                html.Span('Average ACT Score', className='key'),
                html.Span(f'{int(info.ACTCMMID)}', className='val'),
            ]),
        ]),
    ])
    return card

def create_college_info(info, graphs, similar_schools, other_info):
    if info.UGDS < 2500:
        size = 'Very Small'
    elif info.UGDS < 5000:
        size = 'Small'
    elif info.UGDS < 7500:
        size = 'Medium'
    elif info.UGDS < 10000:
        size = 'Large'
    else:
        size = 'Very Large'   
    state_status = 'IN' if other_info['state'] == info.STABBR else 'OUT'
    tuition_and_fees = info[f'TUITIONFEE_{state_status}']
    other_expenses = (info.OTHEREXPENSE_ON + info.OTHEREXPENSE_OFF) / 2
    room_and_board = (info.ROOMBOARD_ON + info.ROOMBOARD_OFF) / 2

    card = html.Div(children=[
        html.Div(className='card large', children=[    
            html.Picture(className='thumbnail', children=[
                html.Img(className='category__01', src=f'/assets/images/colleges/{info.IMAGE}')
            ]),
            html.Div(className='card-content', children=[
                ###Get school long name
                html.H3(info.INSTNM, className='college-name'),
                ###Get school description
                html.P(info.LONG_DESCRIPTION, className=''),
            ]),
            
            # chances of being accepted
            html.Div(className='card-content', children=[
                
                html.H4('Chances of being accepted', className='card-section chart-title'),
                ###Gauge
                html.Div(className='chart-container', children=[
                    create_gauge(info['SELECT_CAT'] - rec.rank_student(other_info['gpa'], other_info['sat'], other_info['act']))
                ])
            ]),

            # Overview
            html.Div(className='card-content', children=[
                html.H4('Overview', className='card-section'),
                html.Div(className='two-col', children=[
                    html.Div(className='col-1', children=[
                        
                        html.Div(className='key-val', children=[
                            html.Span('City', className='key'),
                            # df field: CITY, STABBR 
                            html.Span(f'{info.CITY}, {info.STABBR}', className='val'),
                        ]),
                        
                        html.Div(className='key-val', children=[
                            html.Span('Website', className='key'),
                            # df field: INSTURL
                            html.A(info.INSTURL, href=info.INSTURL, target='_blank', className='val'),
                        ]),
                        html.Div(className='key-val', children=[
                            html.Span('School Type', className='key'),
                            html.Span('Public' if info.CONTROL == 1 else 'Private', className='val'),
                        ]),

                        html.Div(className='key-val', children=[
                            html.Span('Setting', className='key'),
                            html.Span(locale[info.LOCALE], className='val'),
                        ]),
                    ]),

                    html.Div(className='col-2', children=[
                        html.Div(className='key-val', children=[
                            html.Span('Size', className='key'),
                            html.Span(size, className='val'),
                        ]),
                        html.Div(className='key-val', children=[
                            html.Span('Status', className='key'),
                            html.Span('Non-Profit' if info.CONTROL <= 2 else 'For-Profit', className='val'),
                        ]),

                        html.Div(className='key-val', children=[
                            html.Span('On-Campus Housing', className='key'),
                            html.Span("Yes" if info.ROOM == 1 else "No", className='val'),
                        ]),
                        
                        html.Div(className='key-val', children=[
                            html.Span('Level of Study', className='key'),
                            html.Span('Undergrad/Graduate' if info.HIGHDEG == 4 else 'Undergrad', className='val'),
                        ]),
                    ])
                ]),
            ]),html.Br(), html.Br(),
            
            # Cost
            html.Div(className='card-content', children=[
                html.H4('Cost', className='card-section'),
                html.Div(className='two-col', children=[
                    html.Div(className='col-1', children=[

                        html.Div(children=[
                            html.Span('Average Net Price 2019/2020', className='item-header'),
                            html.Span(f'${int(tuition_and_fees + info["BOOKSUPPLY"] + room_and_board + other_expenses):,}', className='item-info'),
                        ]),

                        html.Div(className='key-val', children=[
                            html.Span('Tuition/Fees', className='key'),
                            html.Span(f'${int(tuition_and_fees):,}', className='val'),
                        ]),
                        
                        html.Div(className='key-val', children=[
                            html.Span('Room and Board', className='key'),
                            html.Span(f'${int(room_and_board):,}', className='val'),
                        ]),
                        
                        html.Div(className='key-val', children=[
                            html.Span('Books and Supplies', className='key'),
                            html.Span(f'${int(info.BOOKSUPPLY):,}', className='val'),
                        ]),
                        
                        html.Div(className='key-val', children=[
                            html.Span('Other Expenses', className='key'),
                            html.Span(f'${int(other_expenses):,}', className='val'),
                        ]),
                        html.P(f'Net price is indicative of what it actually costs to attend {info.INSTNM} when typical grants and scholarships are considered. The net price varies by family income and financial need.', className=''),
                        html.Div(children=[
                            html.Span('Expected Salary', className='item-header'),
                            html.Span(f'${int(other_info["exp-salary"]):,} ', className='item-info'),
                            html.P(other_info['exp-salary-desc'])
                        ])
                    ]),

                    html.Div(className='col-2', children=[
                        dcc.Graph(figure = graphs['cost']),
                        dcc.Graph(figure = graphs['earnings'])
                    ])
                ]),
            ]),html.Br(), html.Br(),
            
            # Diversity
            html.Div(className='card-content', children=[
                html.H4('Student Diversity', className='card-section'),
                html.Div(children=[
                    html.Span('Diversity Index Rating', className='item-header'),
                    html.Span(other_info['diversity'], className='item-info'),
                ]),
                html.Div(className='two-col', children=[
                    html.Div(className='col-1', children=[
                        dcc.Graph(figure=graphs['race']),
                        dcc.Graph(figure=graphs['age'])
                    ]),

                    html.Div(className='col-2', children=[
                        dcc.Graph(figure=graphs['sex']),
                        dcc.Graph(figure=graphs['income'])
                    ])
                ]),
            ]),html.Br(), html.Br(),
            
            # Weather 
            html.Div(className='card-content', children=[
                html.H4('Weather', className='card-section'),
                html.Div(className='two-col', children=[
                    html.Div(className='col-1', children=[
                       html.Div(className='key-val', children=[
                           html.Span('Climate Zone', className='key'),
                           html.Span(climate_zone_groups_inv[info['CLIMATE_ZONE_GROUP']], className='val'),
                       ]),
                       html.Div(className='key-val', children=[
                           html.Span('Rain', className='key'),
                           html.Span(level_to_rainy[info['RAINY']], className='val'),
                           html.Img(src='/assets/images/icons/'+"rainy_"+str(info['RAINY'])+'.png', className='rowimg')
                       ]),
                       html.Div(className='key-val', children=[
                           html.Span('Snow', className='key'),
                           html.Span('Yes' if info['SNOWY'] == 1 else 'No', className='val'),
                           html.Img(className='rowimg', src='/assets/images/icons/'+"snowy_"+str(info["SNOWY"])+'.png'),
                           
                       ]),
                    ]),

                    html.Div(className='col-2', children=[
                        html.Div(className='key-val', children=[
                            html.Span('Sun', className='key'),
                            html.Span(level_to_sunny[info['SUNNY']], className='val'),
                            html.Img(className='rowimg', src='/assets/images/icons/'+"sunny_"+str(info["SUNNY"])+'.png'),
                        ]),
                        html.Div(className='key-val', children=[
                            html.Span('Humidity', className='key'),
                            html.Span(level_to_humidity[info['HUMIDITY']], className='val'),
                            html.Img(className='rowimg', src='/assets/images/icons/'+"humidity_"+str(info["HUMIDITY"])+'.png'),
                        ]),
                        html.Div(className='key-val', children=[
                            html.Span('Summers', className='key'),
                            html.Span(level_to_hot_summer[info['HOT_SUMMER']], className='val'),
                            html.Img(className='rowimg', src='/assets/images/icons/'+"hot_summer_"+str(info["HOT_SUMMER"])+'.png'),
                        ])
                    ])
                ])
            ]),
        ]),html.Br(), html.Br(),

        html.H3('Similar Colleges'),

        html.Div(className='cards', children=[
            create_school_card(similar_schools.iloc[i, :]) for i in range(min(4, similar_schools.shape[0]))
        ])

    ])
    return card


##############################  Page 1 ##############################
pageheader = html.Header(children=[
    html.Div(className='flex container', children=[
        html.Img(src=LOGO, height="90px"),
        html.A(href='/1', children=[
            html.Span('College', className='logo-text-1'),
            html.Span('Recommendation Tool', className='logo-text-2'),
        ]),
    ])
])

page1Content = html.Main(children=[
    html.Div(className='flexcols container', children=[
        # col 1
        html.Div(children=[
            html.H3('User Information'),
            html.Div(children=[
                html.Label('Select your desired major'),
                dcc.Dropdown(majors, id='major-i', optionHeight=80, value=None),
                html.Br(),
                
                html.Label('Enter your home ZIP code'),
                dcc.Input(placeholder='ZIP Code', type='number', min=1, max=99950, value=None, id='zip-i', debounce=True),
                html.Br(),

                html.Label('Enter your unweighted GPA'),
                dcc.Input(type='number', min=0, max=4, value=None, id='gpa-i', debounce=True),
                html.Br(),
            
                html.Label('Enter your SAT score'),
                dcc.Input(type='number', value=None, id='sat-i', debounce=True),
                html.Br(),
            
                html.Label('Enter your ACT score'),
                dcc.Input(type='number', value=None, id='act-i', debounce=True),
                html.Br(),
            ])
        ]),

        # col 2
        html.Div(children=[
            html.H3('Specific College Preferences'),
            html.Div(children=[
                html.Label('Select your preferred state'),
                dcc.Dropdown(id='state-i', value=None, options=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']),
                create_slider('state'),
                html.Hr(),html.Br(),
                
                html.Label('Select your desired school size'),
                dcc.Slider(1, 5, 1, value=3, marks={1:'Small', 3:'Medium', 5:'Large'}, id='ugds-i', className='slider'),
                create_slider('ugds'),
                html.Hr(),html.Br(),
                
                html.Label('Select your desired school environment'),
                dcc.Dropdown(['City', 'Suburb', 'Town', 'Rural'], id='locale-first-i', value=None),
                create_slider('locale-first'),
                html.Hr(), html.Br(),

                html.Label('Select your desired weather'),
                dcc.Dropdown(id='climate-zone-i', value=None, placeholder='Climate Zone', options=list(climate_zone_groups.keys())),
                dcc.Dropdown(id='hot-summer-i', value=None, placeholder='Summer Temperature', options=['Cool', 'Moderate', 'Warm', 'Hot']),
                dcc.Dropdown(id='humidity-i', value=None, placeholder='Humidity', options=['Dry', 'Moderate', 'Humid', 'Very Humid']),
                dcc.Dropdown(id='sunny-i', value=None, placeholder='Sunshine', options=['Cloudy', 'Some Sun', 'Very Sunny']),
                dcc.Dropdown(id='rainy-i', value=None, placeholder='Rain', options=['Desert', 'Low', 'Moderate', 'Rainy']),
                dcc.Dropdown(id='snowy-i', value=None, placeholder='Snowy Winters', options=['Yes', 'No']),
                create_slider('weather'),
            ])
        ]),

        # col 3
        html.Div(children=[
            html.H3('Additional Preferences'),
            html.Div(children=[
                html.Label('How important is a low tuition cost to you?'),
                create_slider('tuition'),
                html.Br(),
                html.P('How important is school selectivity to you?'),
                create_slider('select'),
                html.Br(),
                html.P('How important is teaching quality to you?'),
                create_slider('teach-qual'),
                html.Br(),
                html.P('How important is projected earnings to you?'),
                create_slider('exp-earnings'),
                html.Br(),
                html.P('How important is student diversity to you?'),
                create_slider('diversity')
            ])
        ])
    ])
])

page_1_layout = html.Div(children=[
    pageheader,
    page1Content,
    html.Hr(),
    html.Div(className='flex container bottom', children=[
        dcc.Link(html.Button('Submit', className='submit-btn'), href='/2')
    ])
])


##############################  Page 2 ##############################
page2Content = html.Main(children=[
    # html.Div(className='flexcols container', children=[
    #     html.H2('Recommendations')
    # ]),
    html.Div(className='flexcols container', children=[
        # sidebar
        html.Div(className='sidebar', children=[
            html.H3('Filters'),
            html.Div(children=[
                html.H4('Location'),
                
                html.Label('ZIP Code'),
                dcc.Input(placeholder='ZIP Code', type='number', min=1, max=99950, value='', id='zip-ii', debounce=True),
                
                html.Label('Distance From ZIP Code'),
                dcc.Dropdown(['5 miles','10 miles','25 miles','50 miles','100 miles','250 miles','500 miles'],
                id='distance'),
                html.Hr(),

                html.Label('State'),
                dcc.Dropdown(['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'], id='state-ii'),
                html.Br(),

                html.H4('Cost/Earnings'),
                
                html.Label('Tuition'),
                dcc.RangeSlider(0, 50000, step=10000, value=[0, 50000], id='tuition-ii'),
                html.Hr(),
                html.Label('Max Application Fee'),
                dcc.Dropdown(id='applfeeu-ii', options=[0, 20, 40, 60, 80, 100]),
                html.Hr(),
                html.Label('Projected Salary'),
                dcc.RangeSlider(0, 125000, step=25000, value=[0, 125000], id='exp-earnings-ii'),
                html.Br(),
                
                html.H4('Acceptance Chance'),
                dcc.Checklist(id='select-cat-ii', options=['Safety Schools', '50/50 Schools', 'Reach Schools'], value=['Safety Schools', '50/50 Schools', 'Reach Schools']),
                
                html.H4('Weather'),
                
                html.Label('Climate Zone'),
                dcc.Dropdown(id='climate-zone-ii', options=['Tropical', 'Arid', 'Temperate', 'Continental']),
                html.Hr(),
                html.Label('Summer Temperature'),
                dcc.Dropdown(id='hot-summer-ii', options=['Cool', 'Moderate', 'Warm', 'Hot']),
                html.Hr(),
                html.Label('Humidity'),
                dcc.Dropdown(id='humidity-ii', options=['Dry', 'Moderate', 'Humid', 'Very Humid']),
                html.Hr(),
                html.Label('Sunshine'),
                dcc.Dropdown(id='sunny-ii', options=['Cloudy', 'Some Sun', 'Very Sunny']),
                html.Hr(),
                html.Label('Rain'),
                dcc.Dropdown(id='rainy-ii', options=['Desert', 'Low', 'Moderate', 'Rainy']),
                html.Hr(),
                html.Label('Snow'),
                dcc.Dropdown(id='snowy-ii', options=['Yes', 'No']),
                
                html.Br(),
                dcc.Link(html.Button('Apply Filters', className='submit-btn block'), href='/2/filter'),
                html.Br(),
                dcc.Link(html.Button('Clear Filters', className='submit-btn block'), href='/2/filter0')
            ])
        ]),

        # main content
        html.Div(className='main-section', children=[
            html.H3('Recommendations', id='page-2-title'),
            html.Div(className='cards', id='page-2-main'),
            
        ]),
        

    ]),

    html.Div(className='container', children=[
        html.Div(id='map'),
    ]),
])

page_2_layout = html.Div([
    pageheader,
    page2Content,
    # html.H3('Recommendations'),
    # html.Div(id='2c'),
    # html.Div(id='map'),
    # dcc.Link(html.Button('Back'), href='/1'),
])

##############################  Page 3 ##############################
page3Content = html.Main(children=[
    html.Div(className='flexcols container', children=[
        # left sidebar
        #html.Div(className='sidebar'),

        # main content
        html.Div(className='main-section', children=[
            html.H3('College Information', id='page-3-title'),
            html.Div(className='', id='page-3-main')
        ]),

        # right sidebar
        #html.Div(className='sidebar'),
    ])
])

page_3_layout = html.Div(id='page-3-layout', children=[
    pageheader,
    page3Content
])