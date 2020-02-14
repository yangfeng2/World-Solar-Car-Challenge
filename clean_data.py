import pandas as pd
import numpy as np
from glob import glob
import os

# match file pathnames recursively in 'weather_data' directory
for filename in glob(r'..\data\weather_data\*.txt'):
    columns = ['id', 'station_number', 'year', 'month', 'day', 'hour', 'minute', 'precipitation',
               'air_temp', 'dew_point', 'humidity', 'wind_speed', 'wind_speed_quality', 'wind_direction']

    df = pd.read_csv(filename, header=0, names=columns)
    del df['id']

    # merging year, month, day, hour, min columns into a single - date column
    df.day = df.day.transform(lambda i: "{0:0>2d}".format(i))
    df.hour = df.hour.transform(lambda i: "{0:0>2d}".format(i))
    df.minute = df.minute.transform(lambda i: "{0:0>2d}".format(i))
    df['date'] = df.year.map(str) + '-' + df.month.map(str) + '-' + \
        df.day.map(str) + ' ' + df.hour.map(str) + ':' + df.minute.map(str)

    # removing redundant columns
    del df['year'], df['month'], df['day'], df['hour'], df['minute'], df['wind_speed_quality']

    # timeseries data
    df['date'] = pd.to_datetime(df.date)
    df.set_index('date', drop=True, inplace=True)
    df = df.sort_index()

    # dealing with datatypes
    for column in df:
        df[column] = df[column].transform(str)
        df[column] = df[column].str.strip()
        df[column].replace("", np.nan, inplace=True)

        if column == 'station_number' or column == 'wind_speed' or column == 'wind_direction' or column == 'humidity':
            # -1 value denotes missing values
            df[column].fillna(-1, inplace=True)
            df[column] = df[column].astype('int')
        else:
            df[column] = df[column].astype('float')

    # saving 'cleaned' file into 'cleaned_weather_data' directory
    df.to_csv(r'..\data\cleaned_weather_data\\' +
              os.path.splitext(os.path.basename(filename))[0] + '.csv')
