from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import pandas as pd


class WebScraper:
    __location_codes = {
        'Darwin Airport': 'darwin/YPDN/',
        'Alice Springs Airport': 'alice-springs/YBAS/'
    }
    __base_url = 'http://www.wunderground.com/'

    def get_data(self, location):
        """ Parse the html doc using BeautifulSoup for weather data """

        # today's date
        current_date = datetime.today().strftime('%Y-%m-%d')
        url = self.__base_url + 'history/daily/au/' + \
            self.__location_codes[location] + 'date/' + current_date

        html = self.__get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        # parsing the dynamic page
        table = soup.find('table', {'class': 'mat-table ng-star-inserted'})

        dict = {}
        for i in range(10):
            dict[i] = []

        rows = table.tbody.find_all('tr')

        for row in rows:
            columns = row.find_all('td')
            for i in range(len(columns)):
                dict[i].append(columns[i].span.text)

        df = pd.DataFrame(dict)
        df.rename(columns={0: 'Time', 1: 'Temperature', 2: 'Dew Point', 3: 'Humidity', 4: 'Wind',
                           5: 'Wind Speed', 6: 'Wind Gust', 7: 'Pressure', 8: 'Precip.', 9: 'Condition'}, inplace=True)

        # getting live data
        url = self.__base_url + 'weather/au/' + self.__location_codes[location]

        request = Request(url, headers={
            'User-Agent': 'APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html'})

        response = urlopen(request)
        live_data = self.__get_live_data(response)

        return live_data, df

    def __get_live_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # TODO: wind and precipitation data missing
        timestamp = soup.find('p', {'class': 'timestamp'}).strong.text.strip()
        current_temp = soup.find('span', {
                                 'class': 'test-true wu-unit wu-unit-temperature is-degree-visible ng-star-inserted'}).text.replace(u'\xa0', u' ')
        current_dew_point = soup.find('span', {
                                      'class': 'test-false wu-unit wu-unit-temperature ng-star-inserted'}).text.replace(u'\xa0', u' ')
        current_humidity = soup.find('span', {
                                     'class': 'test-false wu-unit wu-unit-humidity ng-star-inserted'}).text.replace(u'\xa0', u' ')
        current_pressure = soup.find('span', {
                                     'class': 'test-false wu-unit wu-unit-pressure ng-star-inserted'}).text.replace(u'\xa0', u' ')
        current_condition = soup.find(
            'div', {'class': 'condition-icon small-6 medium-12 columns'}).p.text

        return {
            'timestamp': timestamp,
            'temperature': current_temp,
            'dew point': current_dew_point,
            'humidity': current_humidity,
            'pressure': current_pressure,
            'condition': current_condition
        }

    def __get_html(self, url):
        """ Retrieve the dynamic html content at the specified url """

        # TODO: make it platform independent
        driver = webdriver.Firefox(
            executable_path=r'../other/geckodriver.exe')
        driver.get(url)
        html = driver.execute_script(
            'return document.documentElement.outerHTML')
        driver.quit()

        return html


if __name__ == '__main__':
    webscraper = WebScraper()
    live, history_df = webscraper.get_data('Darwin Airport')
    print(live)
    print(history_df)
