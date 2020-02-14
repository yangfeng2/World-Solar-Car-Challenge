import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import prototype as graph
from prototype import kde


import numpy as np
import pandas as pd
import datetime
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime as dt
import pathlib

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True

# create KDE instance
self_kde = kde.KDE(bandwidth=0.7, kernel='epanechnikov')

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()


# MapBox API
mapbox_access_token = "pk.eyJ1IjoieWFuZ2ZlbmcyIiwiYSI6ImNrNHRhYml5MTBmMjgzZXJzdTA5cDdzc2cifQ.GUuaKP46IxEjy-18MqHhDw"

# Latitude and Longitude for the main station - hover show latitude and Longitude
fig = go.Figure(go.Scattermapbox(
        lat=['-12.4634','-14.4521','-16.2533','-19.6484'
        ,'-21.3799','-23.698','-25.8436','-29.0135',
        '-30.9678','-32.4952','-34.9285'],
        lon=['130.8445','132.2715','133.3692','134.19','133.9756',
        '133.8807','133.2879','134.7544','135.7593','137.7894','138.6007'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10
        ),
        text=["Darwin","Katherine","Daly Waters","Tennant Creek","Barrow Creek",
        "Alice Springs", "Kulgera", "Cooper Pedy", "Glendambo", "Port Augusta", "Adelaide"],
    ))

# # Map Design
fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=-25.2744,
            lon=133.7751
        ),
        style='satellite',
        pitch=0,
        zoom=3.5
    ),
)


# Top part - top icon and welcoming message
def description_card():
    return html.Div(
        id="description-card",
        children=[
            html.H3("Welcome to the Australia World Solar Car Challenge",style={'text-align':'center'}),
            html.Div(
                id="intro",
                children="Explore Solar system stations weather. Click on the checklist to select the weather you want .",
            ),
        ],
    )
def Map():
    return html.Div(
        id="Mapcontrol",
        children=[
            dcc.Graph(id='graph',style={'height': 700, 'width': 'auto', 'margin': 'auto'},figure=fig,config={'scrollZoom': False}),
        ],
    )
# Australia Map part - display racing route on the map
def StationControl():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="Select - Station",
        children=[
            html.H6("Select a Station"),
            dcc.Dropdown(

                                        id='station',
                                        options=[
                                            {'label': 'Darwin', 'value': 'Darwin Airport'},
                                            {'label': 'Katherine', 'value': 'Bachelor'},
                                            {'label': 'Daly Waters', 'value': 'Daly Waters Airstrip'},
                                            {'label': 'Tennant Creek', 'value': 'Tennant Creek'},
                                            {'label': 'Barrow Creek', 'value': 'Center Island'},
                                            {'label': 'Alice Springs', 'value':'Alice Springs Airport'},
                                            {'label': 'Kulgera', 'value':'Woomera Aerodrome'},
                                            {'label': 'Cooper Pedy', 'value':'Coober Pedy Airport'},
                                            {'label': 'Glendambo', 'value':'Parafield Airport'},
                                            {'label': 'Port Augusta', 'value':'Edinburgh Airport'},
                                            {'label': 'Adelaide', 'value':'Adelaide Airport'}
                                        ],
                                    value='Darwin Airport',
                                    style={'margin-top':30,'margin-left':10,'width':500}),
            ],
    )
# def ModeControl():
#     return html.Div(
#         id="Mode-option",
#         children=[html.P("Select the current WIFI mode"),
#                   dcc.Tab(label='Historical Data (no wifi)', value='tab-1'),
#                   dcc.Tab(label='Live Data (with wifi)', value='tab-2')]
#     )
def ConditionControl():
    """
        :return: A Div containing controls for graphs.
        """
    return html.Div(
        id="Select - Option",
        children=[
            html.H6("Select Weather "),
            dcc.RadioItems(
                id="type_of_data",
                options=[
                    {'label': 'Temperature  ', 'value': 'air_temp'},
                    {'label': 'Dew point ', 'value': 'dew_point'},
                    {'label': 'Humidity ', 'value': 'humidity'},
                    {'label': 'Wind Speed', 'value': 'wind_speed'},
                    {'label': 'Wind Direction', 'value': 'wind_direction'},
                ],
                style={'margin-left': 20, 'font-size': 20, 'color': '#2c8cff', 'line-height': 30},
                value='air_temp'
            ),
        ]
    )
def DateControl():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="Select - Time",
        children=[
            html.H6("Select Date and hour"),
            dcc.DatePickerSingle(
                id="day_of_month",
                min_date_allowed=dt(2021, 10, 1),
                max_date_allowed=dt(2021, 10, 31),
                initial_visible_month=dt(2021, 10, 1),
                date=str(dt(2021, 10, 1, 23, 59, 59)),
                style={'margin-left':20},
                display_format='D/M/Y',
            ),
            ],
    )
def TimeControl():
    return html.Div(
        id="submit",
        children=[
            dcc.Dropdown(
                id='hour_of_day',
                        options=[
                            {'label': '00:00', 'value': '0'},
                            {'label': '01:00', 'value': '1'},
                            {'label': '02:00', 'value': '2'},
                            {'label': '03:00', 'value': '3'},
                            {'label': '04:00', 'value': '4'},
                            {'label': '05:00', 'value': '5'},
                            {'label': '06:00', 'value': '6'},
                            {'label': '07:00', 'value': '7'},
                            {'label': '08:00', 'value': '8'},
                            {'label': '09:00', 'value': '9'},
                            {'label': '10:00', 'value': '10'},
                            {'label': '11:00', 'value': '11'},
                            {'label': '12:00', 'value': '12'},
                            {'label': '13:00', 'value': '13'},
                            {'label': '14:00', 'value': '14'},
                            {'label': '15:00', 'value': '15'},
                            {'label': '16:00', 'value': '16'},
                            {'label': '17:00', 'value': '17'},
                            {'label': '18:00', 'value': '18'},
                            {'label': '19:00', 'value': '19'},
                            {'label': '20:00', 'value': '20'},
                            {'label': '21:00', 'value': '21'},
                            {'label': '22:00', 'value': '22'},
                            {'label': '23:00', 'value': '23'},
                            {'label': '24:00', 'value': '24'},
                ],
                style={'width': 135, 'height': 30, 'margin-top': 10,'margin-left':10},
                value=1
            ),
        ],
    )
def SubmitControl():
    """
        :return: A Div containing controls for graphs.
        """
    return html.Div(
        id="Submit",
        children=[
            html.Button(id="submit-btn", children="Submit", style={"margin-top": 30}, n_clicks=0),
        ],
        style={'margin-left':20},
    )
# layout of the page
app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("logo.png"))],
        ),
        html.Div(
            id="Welcome",
            className="welcome",
            children=[description_card()]
        ),
        html.Div(
            id="Map",
            className="MapDisplay",
            children=[Map()]
        ),
        html.Div(
            id = "Center-left",
            className="Centerl",
            children=[
                StationControl(),DateControl(),TimeControl(),html.Br(),html.Br(),dcc.Graph(id="history-graph",style={'width':600}),
                ]


        ),
        html.Div(
            id="Center-right",
            className="Centerr",
            children=[ConditionControl(),dcc.Graph(id="weather-graph",style={'width':600,'margin-top':75}),
                        ]

        ),
        html.Div(
            id = "bottom-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="graph-display",
                    children=[
                        
                        
                    ],
                ),
            ],
        ),
    ],
)
@app.callback(
    dash.dependencies.Output("weather-graph","figure"),
    [dash.dependencies.Input("day_of_month","date"),
     dash.dependencies.Input("hour_of_day","value"),
     dash.dependencies.Input("type_of_data","value"),
     dash.dependencies.Input("station","value")]
)
def update_graph(date,input_hour,input_type,station):
    
    date = dt.strptime(date.split(' ')[0],'%Y-%m-%d')
    date_string = date.strftime('%d')

    self_kde.fit(station, str(input_type),int(date_string), int(input_hour))
    self_kde_data = self_kde.sample(200)
    
    _locationsName = {
                    'air_temp':'Air Temperature (°C)',
                    'dew_point':'Dew Point',
                    'humidity':'Humidity (%)',
                    'wind_speed':'Wind Speed (mph)',
                    'wind_direction':'Wind Direction (Degree °)',
                    'solar':'Solar',
                    'pressure':'Pressure',
                }

    return {
        'data': [dict(
            
            x=self_kde_data.x_values,
            y=self_kde_data.y_values
        )],
        'layout': dict(
            title='Prediction Model',
            xaxis={
                'title': _locationsName[input_type],
            },
            yaxis={
                'title': 'Probability Density',
            }
        )

    }

@app.callback(
    dash.dependencies.Output("history-graph","figure"),
    [dash.dependencies.Input("day_of_month","date"),
     dash.dependencies.Input("hour_of_day","value"),
     dash.dependencies.Input("type_of_data","value"),
     dash.dependencies.Input("station","value")]
)
def update_history_graph(date,input_hour,input_type,station):
    
    __locations = {
        'Darwin Airport': '014015',
        'Bachelor': '014272',
        'Noonamah Airstrip': '014314',
        'Daly Waters Airstrip': '014626',
        'Center Island': '014703',
        'RAAF Base Tindal': '014932',
        'Kangaroo Flats': '014982',
        'Tennant Creek': '015135',
        'Alice Springs Airport': '015590',
        'Woomera Aerodrome': '016001',
        'Coober Pedy Airport': '016090',
        'Port Pirie Aerodrome': '021139',
        'Parafield Airport': '023013',
        'Adelaide Airport': '023034',
        'Edinburgh Airport': '023083'
    }

    # Get the file location
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    DATA_PATH2 = DATA_PATH.joinpath("cleaned_weather_data").resolve()
    filename = __locations[station]
    # read the csv
    df = pd.read_csv(str(DATA_PATH2) + '/' +
                filename + '.csv', index_col='date')
    # change index to datetime
    df.index = pd.DatetimeIndex(df.index)
    # get the day, hour and minute
    date = dt.strptime(date.split(' ')[0],'%Y-%m-%d')
    _day = date.strftime('%d')



    df = df[(df.index.day==int(_day))&(df.index.hour==int(input_hour))&(df.index.minute==0)]
    

    _locationsName = {
                    'air_temp':'Air Temperature (°C)',
                    'dew_point':'Dew Point',
                    'humidity':'Humidity (%)',
                    'wind_speed':'Wind Speed (mph)',
                    'wind_direction':'Wind Direction (Degree °)',
                    'solar':'Solar',
                    'pressure':'Pressure',
                }

    #[go.Bar(dict(
    #        x=df.index,
    #        y=df[str(input_type)],
    #    ))],

    return {
        'data': [dict(
            x=df.index,
            y=df[str(input_type)],
        )],
        'layout': dict(
            title='History Data',
            xaxis={
                'title': 'Year'
            },
            yaxis={
                'title': _locationsName[input_type],
            }
        )

    }

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
