import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

pd.options.mode.chained_assignment = None  # disable error message

app = dash.Dash()

df = pd.read_csv(r'../weather_data/014015.txt', delimiter=',', skipinitialspace=True)

app.layout = html.Div([
    html.H1(children='Graphs'),
    html.H3(children='Town:'),
    dcc.Dropdown(
        id='file',
        options=[{'label': 'Darwin Airport', 'value': '014015'},
                 {'label': 'Bachelor', 'value': '014272'},
                 {'label': 'Noonamah Airstrip', 'value': '014314'},
                 {'label': 'Daly Waters Airstrip', 'value': '014626'},
                 {'label': 'Center Island', 'value': '014703'},
                 {'label': 'RAAF Base Tindal', 'value': '014932'},
                 {'label': 'Kangaroo Flats', 'value': '014982'},
                 {'label': 'Tennant Creek', 'value': '015135'},
                 {'label': 'Alice Springs Airport', 'value': '015590'},
                 {'label': 'Woomera Aerodrome', 'value': '016001'},
                 {'label': 'Coober Pedy Airport', 'value': '016090'},
                 {'label': 'Port Pirie Aerodrome', 'value': '021139'},
                 {'label': 'Parafield Airport', 'value': '023013'},
                 {'label': 'Adelaide Airport', 'value': '023034'},
                 {'label': 'Edinburgh Airport', 'value': '023083'}],
        value='014015'
    ),
    html.H3(children='Time frame:'),
    dcc.Dropdown(
        id='time-option',
        options=[{'label': 'All Years', 'value': 'all_years'},
                 {'label': 'Daily', 'value': 'year'},
                 {'label': 'Hourly', 'value': 'daily'}],
        value='all_years'
    ),
    html.H3(children='Attributes:'),
    dcc.RadioItems(
        id='data-type',
        options=[{'label': 'Air Temp', 'value': 'temp'},
                 {'label': 'Dew Point', 'value': 'dew_point'},
                 {'label': 'Precipitation', 'value': 'rain'},
                 {'label': 'Humidity', 'value': 'humid'},
                 {'label': 'Wind Speed', 'value': 'wind_speed'}],
        value='temp'

    ),
    dcc.RadioItems(
        id='max-min',
        options=[{'label': 'Maximum', 'value': 'max'},
                 {'label': 'Average', 'value': 'mean'},
                 {'label': 'Minimum', 'value': 'min'},
                 {'label': 'All', 'value': 'all_stats'}],
        value='all_stats'
    ),

    dcc.Graph(id='graph'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph', 'figure'),
    [Input('file', 'value'),
     Input('time-option', 'value'),
     Input('data-type', 'value'),
     Input('max-min', 'value'),
     Input('year-slider', 'value')])
     
def change_graph(filename, time, data_type, input_data, selected_year):
    df = pd.read_csv(r'../weather_data/' + filename + '.txt', delimiter=',', skipinitialspace=True)
    dff = df[df.year == selected_year]
    # Plots data for a selected year on a selected file
    ####################################################################################
    if time == 'year':
        # Plots Temp, max, mean, min and all
        if data_type == 'temp':
            if input_data == 'max':
                y = dff.groupby(['day'], sort=False)['air_temp'].max()
                colour = 'red'
                stat = 'max'
            elif input_data == 'mean':
                y = dff.groupby(['day'], sort=False)['air_temp'].mean()
                colour = 'green'
                stat = 'average'
            elif input_data == 'min':
                y = dff.groupby(['day'], sort=False)['air_temp'].min()
                colour = 'blue'
                stat = 'min'
            elif input_data == 'all_stats':
                y = dff.groupby(['day'], sort=False)['air_temp'].max()
                yy = dff.groupby(['day'], sort=False)['air_temp'].mean()
                yyy = dff.groupby(['day'], sort=False)['air_temp'].min()

                traces = []

                traces.append(go.Scatter(
                    x=dff['day'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=dff['day'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=dff['day'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Daily Temperature in ' + str(selected_year),
                        xaxis={'title': 'Day'},
                        yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                        hovermode='closest'
                    )
                }
        # Plots dew point temp, max, mean, min and all
        elif data_type == 'dew_point':
            if input_data == 'max':
                y = dff.groupby(['day'], sort=False)['dew_point'].max()
                colour = 'red'
                stat = 'max'
            elif input_data == 'mean':
                y = dff.groupby(['day'], sort=False)['dew_point'].mean()
                colour = 'green'
                stat = 'average'
            elif input_data == 'min':
                y = dff.groupby(['day'], sort=False)['dew_point'].min()
                colour = 'blue'
                stat = 'min'
            elif input_data == 'all_stats':
                y = dff.groupby(['day'], sort=False)['dew_point'].max()
                yy = dff.groupby(['day'], sort=False)['dew_point'].mean()
                yyy = dff.groupby(['day'], sort=False)['dew_point'].min()

                traces = []

                traces.append(go.Scatter(
                    x=dff['day'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=dff['day'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=dff['day'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Daily Dew Point Temperature in ' + str(selected_year),
                        xaxis={'title': 'Day', 'range': [1, 30]},
                        yaxis={'title': 'Dew Point Temperature (C\N{DEGREE SIGN})'},
                        hovermode='closest'
                    )
                }
            traces = []

            traces.append(go.Scatter(
                x=dff['day'].unique(),
                y=y,
                mode='lines+markers',
                line=dict(color=colour),
            ))

            return {
                'data': traces,
                'layout': go.Layout(
                    title='Daily ' + stat + ' Dew Point Temp in ' + str(selected_year),
                    xaxis={'title': 'Day', 'range': [1, 30]},
                    yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                    hovermode='closest'
                )
            }
        # Plots precipitation
        elif data_type == 'rain':
            y = dff.groupby(['day'], sort=False)['precipitation'].max()

            traces = []

            traces.append(go.Bar(
                x=dff['day'].unique(),
                y=y,
            ))

            return {
                'data': traces,
                'layout': go.Layout(
                    title='Total Precipitation per day in ' + str(selected_year),
                    xaxis={'title': 'Day', 'range': [1, 30]},
                    yaxis={'title': 'Precipitation (mm)'},
                    hovermode='closest'
                )
            }

        traces = []

        traces.append(go.Scatter(
            x=dff['day'].unique(),
            y=y,
            mode='lines+markers',
            line=dict(color=colour),
        ))

        return {
            'data': traces,
            'layout': go.Layout(
                title='Daily ' + stat + ' Temp in ' + str(selected_year),
                xaxis={'title': 'Day', 'range': [1, 30]},
                yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                hovermode='closest'
            )
        }
    #####################################################################################
    # Plots Data for all years on selected file
    elif time == 'all_years':
        # Shows Temp, max, mean, min and all
        if data_type == 'temp':
            if input_data == 'max':
                y = df.groupby(['year'], sort=False)['air_temp'].max()
                colour = 'red'
            elif input_data == 'mean':
                y = df.groupby(['year'], sort=False)['air_temp'].mean()
                colour = 'green'
            elif input_data == 'min':
                y = df.groupby(['year'], sort=False)['air_temp'].min()
                colour = 'blue'
            elif input_data == 'all_stats':
                y = df.groupby(['year'], sort=False)['air_temp'].max()
                yy = df.groupby(['year'], sort=False)['air_temp'].mean()
                yyy = df.groupby(['year'], sort=False)['air_temp'].min()

                traces = []

                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Temperature Per Year in October',
                        xaxis={'title': 'Year'},
                        yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                        hovermode='closest'
                    )
                }
        # Shows Dew point temp, max, mean, min and all
        elif data_type == 'dew_point':
            if input_data == 'max':
                y = df.groupby(['year'], sort=False)['dew_point'].max()
                colour = 'red'
            elif input_data == 'mean':
                y = df.groupby(['year'], sort=False)['dew_point'].mean()
                colour = 'green'
            elif input_data == 'min':
                y = df.groupby(['year'], sort=False)['dew_point'].min()
                colour = 'blue'
            elif input_data == 'all_stats':
                y = df.groupby(['year'], sort=False)['dew_point'].max()
                yy = df.groupby(['year'], sort=False)['dew_point'].mean()
                yyy = df.groupby(['year'], sort=False)['dew_point'].min()

                traces = []

                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Dew Point Temperature',
                        xaxis={'title': 'Year'},
                        yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                        hovermode='closest'
                    )
                }
        # Plots total precipitation in October
        elif data_type == 'rain':
            y = df.groupby(['year'], sort=False)['precipitation'].sum()

            traces = []

            traces.append(go.Bar(
                x=df['year'].unique(),
                y=y,
            ))

            return {
                'data': traces,
                'layout': go.Layout(
                    title='Total Precipitation Per Year in October',
                    xaxis={'title': 'Year'},
                    yaxis={'title': 'Precipitation (mm)'},
                    hovermode='closest'
                )
            }
        # Plots humidity
        elif data_type == 'humid':
            if input_data == 'max':
                y = df.groupby(['year'], sort=False)['humidity'].max()
                colour = 'red'
            elif input_data == 'mean':
                y = df.groupby(['year'], sort=False)['humidity'].mean()
                colour = 'green'
            elif input_data == 'min':
                y = df.groupby(['year'], sort=False)['humidity'].min()
                colour = 'blue'
            elif input_data == 'all_stats':
                y = df.groupby(['year'], sort=False)['humidity'].max()
                yy = df.groupby(['year'], sort=False)['humidity'].mean()
                yyy = df.groupby(['year'], sort=False)['humidity'].min()

                traces = []

                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=df['year'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Humidity Per Year in October',
                        xaxis={'title': 'Year'},
                        yaxis={'title': 'Humidity (%)', 'range': [0, 100]},
                        hovermode='closest'
                    )
                }

            traces = []

            traces.append(go.Scatter(
                x=dff['hour'].unique(),
                y=y,
                mode='lines+markers',
                line=dict(color=colour),
            ))
            return {
                'data': traces,
                'layout': go.Layout(
                    title='Humidity Per Year in October',
                    xaxis={'title': 'Hour (24h)', 'range': [0, 23]},
                    yaxis={'title': 'Humidity (%)', 'range': [0, 100]},
                    hovermode='closest'
                )
            }
        traces = []

        traces.append(go.Scatter(
            x=df['year'].unique(),
            y=y,
            mode='lines+markers',
            line=dict(color=colour),
        ))

        return {
            'data': traces,
            'layout': go.Layout(
                title='Temperature Per Year in October',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                hovermode='closest'
            )
        }
    #####################################################################################
    # Plots daily data based on hour
    elif time == 'daily':
        if data_type == 'temp':
            if input_data == 'max':
                y = dff.groupby(['hour'], sort=False)['air_temp'].max()
                colour = 'red'
            elif input_data == 'mean':
                y = dff.groupby(['hour'], sort=False)['air_temp'].mean()
                colour = 'green'
            elif input_data == 'min':
                y = dff.groupby(['hour'], sort=False)['air_temp'].min()
                colour = 'blue'
            elif input_data == 'all_stats':
                y = dff.groupby(['hour'], sort=False)['air_temp'].max()
                yy = dff.groupby(['hour'], sort=False)['air_temp'].mean()
                yyy = dff.groupby(['hour'], sort=False)['air_temp'].min()

                traces = []

                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Daily Temperature by hour in ' + str(selected_year),
                        xaxis={'title': 'Hour (24)', 'range': [0, 23]},
                        yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                        hovermode='closest'
                    )
                }
        # Shows Dew point temp, max, mean, min and all
        elif data_type == 'dew_point':
            if input_data == 'max':
                y = dff.groupby(['hour'], sort=False)['dew_point'].max()
                colour = 'red'
            elif input_data == 'mean':
                y = dff.groupby(['hour'], sort=False)['dew_point'].mean()
                colour = 'green'
            elif input_data == 'min':
                y = dff.groupby(['hour'], sort=False)['dew_point'].min()
                colour = 'blue'
            elif input_data == 'all_stats':
                y = dff.groupby(['hour'], sort=False)['dew_point'].max()
                yy = dff.groupby(['hour'], sort=False)['dew_point'].mean()
                yyy = dff.groupby(['hour'], sort=False)['dew_point'].min()

                traces = []

                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Daily Dew Point Temperature by Hour in ' + str(selected_year),
                        xaxis={'title': 'Hour (24)', 'range': [0, 23]},
                        yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                        hovermode='closest'
                    )
                }
        # Plots total precipitation in October
        elif data_type == 'rain':
            y = dff.groupby(['hour'], sort=False)['precipitation'].mean()

            traces = []

            traces.append(go.Bar(
                x=dff['hour'].unique(),
                y=y,
            ))

            return {
                'data': traces,
                'layout': go.Layout(
                    title='Average Precipitation by Hour in ' + str(selected_year),
                    xaxis={'title': 'Hour (24 hour)'},
                    yaxis={'title': 'Precipitation (mm)'},
                    hovermode='closest'
                )
            }
        # Plots Humidity
        elif data_type == 'humid':
            if input_data == 'max':
                y = dff.groupby(['hour'], sort=False)['humidity'].max()
                colour = 'red'
            elif input_data == 'mean':
                y = dff.groupby(['hour'], sort=False)['humidity'].mean()
                colour = 'green'
            elif input_data == 'min':
                y = dff.groupby(['hour'], sort=False)['humidity'].min()
                colour = 'blue'
            elif input_data == 'all_stats':
                y = dff.groupby(['hour'], sort=False)['humidity'].max()
                yy = dff.groupby(['hour'], sort=False)['humidity'].mean()
                yyy = dff.groupby(['hour'], sort=False)['humidity'].min()

                traces = []

                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Daily Humidity by Hour in ' + str(selected_year),
                        xaxis={'title': 'Hour (24)', 'range': [0, 23]},
                        yaxis={'title': 'Humidity (%)', 'range': [0, 100]},
                        hovermode='closest'
                    )
                }
            traces = []

            traces.append(go.Scatter(
                x=df['hour'].unique(),
                y=y,
                mode='lines+markers',
                line=dict(color=colour),
            ))

            return {
                'data': traces,
                'layout': go.Layout(
                    title='Daily Humidity by Hour in ' + str(selected_year),
                    xaxis={'title': 'Hour (24)', 'range': [0, 23]},
                    yaxis={'title': 'Humidity (%)', 'range': [0, 100]},
                    hovermode='closest'
                )
            }
        # Plots wind speed
        elif data_type == 'wind_speed':
            if input_data == 'max':
                y = dff.groupby(['hour'], sort=False)['wind_speed'].max()
                colour = 'red'
            elif input_data == 'mean':
                y = dff.groupby(['hour'], sort=False)['wind_speed'].mean()
                colour = 'green'
            elif input_data == 'min':
                y = dff.groupby(['hour'], sort=False)['wind_speed'].min()
                colour = 'blue'
            elif input_data == 'all_stats':
                y = dff.groupby(['hour'], sort=False)['wind_speed'].max()
                yy = dff.groupby(['hour'], sort=False)['wind_speed'].mean()
                yyy = dff.groupby(['hour'], sort=False)['wind_speed'].min()

                traces = []

                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red'),
                    name='Max',
                ))
                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=yy,
                    mode='lines+markers',
                    line=dict(color='green'),
                    name='Mean',
                ))
                traces.append(go.Scatter(
                    x=dff['hour'].unique(),
                    y=yyy,
                    mode='lines+markers',
                    line=dict(color='blue'),
                    name='Min',
                ))

                return {
                    'data': traces,
                    'layout': go.Layout(
                        title='Daily Wind Speed by Hour in ' + str(selected_year),
                        xaxis={'title': 'Hour (24)', 'range': [0, 23]},
                        yaxis={'title': 'Wind speed in Km/h'},
                        hovermode='closest'
                    )
                }

        traces = []

        traces.append(go.Scatter(
            x=dff['hour'].unique(),
            y=y,
            mode='lines+markers',
            line=dict(color=colour),
        ))
        return {
            'data': traces,
            'layout': go.Layout(
                title='Temperature by Hour in ' + str(selected_year),
                xaxis={'title': 'Hour (24h)', 'range': [0, 23]},
                yaxis={'title': 'Temperature (C\N{DEGREE SIGN})'},
                hovermode='closest'
            )
        }


if __name__ == '__main__':
    app.run_server(debug=True)
