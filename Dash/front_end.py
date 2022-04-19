from dash import html, dcc


majors = ["Agriculture, Agriculture Operations, And Related Sciences", "Natural Resources And Conservation", "Architecture And Related Services", "Area, Ethnic, Cultural, Gender, And Group Studies", "Communication, Journalism, And Related Programs", "Communications Technologies/Technicians And Support Services", "Computer And Information Sciences And Support Services", "Personal And Culinary Services", "Education", "Engineering", "Engineering Technologies And Engineering-Related Fields", "Foreign Languages, Literatures, And Linguistics",	"Family And Consumer Sciences/Human Sciences", "Legal Professions And Studies", "English Language And Literature/Letters", "Liberal Arts And Sciences, General Studies And Humanities", "Library Science", "Biological And Biomedical Sciences", "Mathematics And Statistics", "Military Technologies And Applied Sciences", "Multi/Interdisciplinary Studies",	"Parks, Recreation, Leisure, And Fitness Studies", "Philosophy And Religious Studies", "Theology And Religious Vocations", "Physical Sciences", "Science Technologies/Technicians", "Psychology", "Homeland Security, Law Enforcement, Firefighting And Related Protective Services", "Public Administration And Social Service Professions", "Social Sciences", "Construction Trades", "Mechanic And Repair Technologies/Technicians", "Precision Production", "Transportation And Materials Moving", "Visual And Performing Arts", "Health Professions And Related Programs", "Business, Management, Marketing, And Related Support Services", "History"]
climate_zones = {'Tropical (examples: Honolulu and Miami)':'A', 'Arid (examples: Pheonix and Denver)':'B', 'Temperate (examples: San Francisco and Atlanta)':'C', 'Continental (examples: Boston and Detroit)':'D'}
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

def create_school_card(info):
    card = html.A(className='card', href=f'/college/{info.UNITID}', children=[
        html.Picture(className='thumbnail', children=[
            ###Get school picture
            html.Img(className='category__01', src=f'/assets/images/colleges/{info.IMAGE}')
        ]),
        html.Div(className='card-content', children=[
            ###Get school long name
            html.H4(f'{info.INSTNM}', className=''),
            html.H5(f'{info.CITY}, {info.STABBR}')
        ]),
        html.Footer(className='card-footer', children=[
            html.Div(className='post-meta', children=[
                html.Span(className='', children=[
                    html.P(f'Required GPA: {info.GPA_BOTTOM_TEN_PERCENT}'),
                    html.P(f'Average SAT Score: {info.SAT_AVG}'),
                    html.P(f'Average ACT Score: {info.ACTCMMID}')
                ])
            ])
        ])
    ])
    return card

def create_college_info(info, users_state):
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
    state_status = 'IN' if users_state == info.STABBR else 'OUT'
    tuition_and_fees = info[f'TUITIONFEE_{state_status}']
    other_expenses = (info.OTHEREXPENSE_ON + info.OTHEREXPENSE_OFF) / 2
    room_and_board = (info.ROOMBOARD_ON + info.ROOMBOARD_OFF) / 2

    card = html.Div(className='card large', children=[    
        html.Picture(className='thumbnail', children=[
            html.Img(className='category__01', src=f'/assets/images/colleges/{info.IMAGE}')
        ]),
        html.Div(className='card-content', children=[
            ###Get school long name
            html.H3(info.INSTNM, className='college-name'),
            ###Get school description
            html.P(info.LONG_DESCRIPTION, className=''),
        ]),

        # Overview
        html.Div(className='card-content', children=[
            html.H4('Overview', className='card-section'),
            html.Div(className='two-col', children=[
                html.Div(className='col-1', children=[

                    html.Div(children=[
                        html.Span('Student Population', className='item-header'),
                        html.Span(f'{info.UGDS}', className='item-info'),
                    ]),

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
                    html.Div(children=[
                        html.Span('Best College Rank', className='item-header'),
                        html.Span("NOT IMPLEMENTED (WE DON'T HAVE THIS DATA)", className='item-info'),
                    ]),

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
            html.P(info.LONG_DESCRIPTION, className=''),
        ]),

        # Cost
        html.Div(className='card-content', children=[
            html.H4('Cost', className='card-section'),
            html.Div(className='two-col', children=[
                html.Div(className='col-1', children=[

                    html.Div(children=[
                        html.Span('Sticker Price', className='item-header'),
                        html.Span('NOT EXACTLY SURE WHAT THIS SHOULD BE', className='item-info'),
                    ]),

                    html.Div(className='key-val', children=[
                        html.Span('Tuition/Fees', className='key'),
                        html.Span('$'+str(tuition_and_fees), className='val'),
                    ]),
                    
                    html.Div(className='key-val', children=[
                        html.Span('Books and Supplies', className='key'),
                        html.Span(f'${info.BOOKSUPPLY}', className='val'),
                    ]),

                    html.Div(className='key-val', children=[
                        html.Span('Other Fees', className='key'),
                        html.Span('THIS IS INCLUDED IN Tuition/Fees', className='val'),
                    ]),
                ]),

                html.Div(className='col-2', children=[
                    html.Div(children=[
                        html.Span('Average Net Price 2019/2020', className='item-header'),
                        html.Span('$' + str(tuition_and_fees + info['BOOKSUPPLY'] + room_and_board + other_expenses), className='item-info'),
                    ]),

                    html.Div(className='key-val', children=[
                        html.Span('Room and Board', className='key'),
                        html.Span('$' + str(room_and_board), className='val'),
                    ]),

                    html.Div(className='key-val', children=[
                        html.Span('Other Expenses', className='key'),
                        html.Span('$' + str(other_expenses), className='val'),
                    ]),

                    # etc


                ])
            ]),
            html.P(f'Net price is indicative of what it actually costs to attend {info.INSTNM} when typical grants and scholarships are considered. The net price varies by family income and financial need.', className=''),
        ]),

        # Etc
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
                html.Label('Select your desired location'),
                dcc.Dropdown(id='state-i', placeholder='Preferred State', options=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']),
                create_slider('state'),
                html.Br(),
                
                html.Label('Select your desired school size'),
                dcc.Slider(1, 5, 1, value=1, marks={1:'Small', 3:'Medium', 5:'Large'}, id='ugds-i', className='slider'),
                create_slider('ugds'),
                html.Br(),
                
                html.Label('Select your desired school environment'),
                dcc.Dropdown(['City', 'Suburb', 'Town', 'Rural'], id='locale-first-i'),
                create_slider('locale-first'),

                html.Label('Select your desired weather'),
                dcc.Dropdown(id='climate-zone-i', placeholder='Climate Zone', options=list(climate_zones.keys())),
                dcc.Dropdown(id='hot-summer-i', placeholder='Summer Temperature', options=['Cool', 'Moderate', 'Warm', 'Hot']),
                dcc.Dropdown(id='humidity-i', placeholder='Humidity', options=['Dry', 'Moderate', 'Humid', 'Very Humid']),
                dcc.Dropdown(id='sunny-i', placeholder='Sunshine', options=['Cloudy', 'Some Sun', 'Very Sunny']),
                dcc.Dropdown(id='rainy-i', placeholder='Rain', options=['Desert', 'Low', 'Moderate', 'Rainy']),
                dcc.Checklist(['Snowy Winters'], id='snowy-i'),
                create_slider('weather'),
                html.Br()
            ])
        ]),

        # col 3
        html.Div(children=[
            html.H3('Additional Preferences'),
            html.Div(children=[
                html.Label('How important is a low tuition cost to you?'),
                create_slider('tuition'),
                html.P('How important is school selectivity to you?'),
                create_slider('select'),
                html.P('How important is teaching quality to you?'),
                create_slider('teach-qual'),
                html.P('How important is projected earnings to you?'),
                create_slider('exp-earnings'),
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
                dcc.Input(placeholder='Zip Code', type='number', min=1, max=99950, value='', id='zip-ii', debounce=True),
                
                html.Label('Distance From ZIP Code'),
                dcc.Dropdown(['5 miles','10 miles','25 miles','50 miles','100 miles','250 miles','500 miles'],
                id='distance'),
                html.Hr(),

                html.Label('State'),
                dcc.Dropdown(['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'], id='state-ii'),
                html.Br(),

                html.H4('Tuition'),
                dcc.Slider(0, 50000, 1, id=f'tuition-ii', value=25000, className='slider',
                    marks={1: '0', 50000: '50000'}),

                html.H4('Minimum Projected Salary'),
                dcc.Input(placeholder='Salary', type='number', min=1, max=99950, value='', id='salary-ii', debounce=True),
                html.Br(),

                html.H4('Admission Charges'),
                dcc.Slider(0, 10000, 1, id=f'admission-cost-ii', value=5000, className='slider', marks={1: '0', 10000: '10000'}),
                html.Br(),

                dcc.Link(html.Button('Submit', className='submit-btn block'), href='/2/filter'),
                html.Br(),
                dcc.Link(html.Button('Reset Filters', className='submit-btn block'), href='/2/filter0')
            ])
        ]),

        # main content
        html.Div(className='main-section', children=[
            html.H3('Recommendations', id='page-2-title'),
            html.Div(className='cards', id='page-2-main')
        ]),

    ]),

    html.Div(className='flexcols container', children=[
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
        html.Div(className='sidebar'),

        # main content
        html.Div(className='main-section', children=[
            html.H3('College Information', id='page-3-title'),
            html.Div(className='', id='page-3-main')
        ]),

        # right sidebar
        html.Div(className='sidebar'),
    ])
])

page_3_layout = html.Div(id='page-3-layout', children=[
    pageheader,
    page3Content
])