from dash import Dash, dcc, html, callback, Output, Input
import sys
sys.path.append('./Dash')
import front_end
import callbacks


app = Dash(__name__,
           title='College Recommendation System',
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],
           suppress_callback_exceptions=True,
           external_stylesheets=['assets/style.css'])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='1s', storage_type='session'),
    dcc.Store(id='2s', storage_type='session'),
    dcc.Store(id='last-page', data='/1', storage_type='session'),
    dcc.Store(id='new-page', data='/1', storage_type='session'),
    html.Div(id='pc', children=front_end.page_1_layout)
])

@callback(Output('pc', 'children'),
          Input('new-page', 'data'))
def change_page(new_page):
    if new_page == '/1':
        return front_end.page_1_layout
    elif new_page == '/2':
        return front_end.page_2_layout
    elif new_page is None or new_page == '':
        return front_end.page_1_layout
    else:
        return front_end.page_3_layout

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)