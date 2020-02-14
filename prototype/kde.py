import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathlib
from sklearn.neighbors import KernelDensity

plt.style.use('ggplot')


class KDE:
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

    def __init__(self, bandwidth=1.0, kernel='gaussian'):
        self.__kernel = kernel
        self.__bw = bandwidth

        self.__model = KernelDensity(kernel=kernel, bandwidth=bandwidth)

    def fit(self, location, column, day_of_month, hour_of_day, resample=True):
        # get folder
        PATH = pathlib.Path(__file__).parent.parent
        DATA_PATH = PATH.joinpath("data").resolve()
        DATA_PATH2 = DATA_PATH.joinpath("cleaned_weather_data").resolve()
        filename = self.__locations[location]
        data = pd.read_csv(str(DATA_PATH2) + '\\' +
                           filename + '.csv', parse_dates=True, index_col='date')
        data = data[column]

        # downsample timeseries data into hourly format
        data = data.resample('H').mean()

        # extract all relevant historical observations
        data = data[data.index.day == day_of_month]
        data = data[data.index.hour == hour_of_day]
        data = data.dropna()
        self.__data_max = data.max()
        self.__data_min = data.min()

        self.__model = self.__model.fit(data.to_numpy().reshape(-1, 1))

    def sample(self, number_of_samples=1000):
        x_plot = np.linspace(self.__data_min - 1,
                             self.__data_max + 1, number_of_samples)
        log_dens = self.__model.score_samples(x_plot.reshape(-1, 1))
        y_plot = np.exp(log_dens)

        return pd.DataFrame({'x_values': x_plot, 'y_values': y_plot})


if __name__ == '__main__':

    dar = pd.read_csv(
        'http://www.sharecsv.com/dl/0ae70ffb5c99d5c854781de81fd6632b/014015.csv', parse_dates=True, index_col='date')
    dar = dar['air_temp']
    dar = dar[dar.index.day == 10]
    dar = dar[dar.index.hour == 8]

    fig, axes = plt.subplots(1, 1)
    axes.hist(dar, density=True, bins=15, alpha=0.4)

    kde = KDE(bandwidth=0.7, kernel='epanechnikov')
    kde.fit('Darwin Airport', 'air_temp', 10, 8)
    kde_data = kde.sample(200)

    print(kde_data.head(50))

    axes.plot(kde_data.x_values, kde_data.y_values, color='b', alpha=0.4)

    plt.show()
