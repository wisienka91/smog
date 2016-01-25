# -*- coding: utf-8 -*-
import json
import requests
import sys
from datetime import datetime


class SmogDataFetcher(object):

    def __init__(self, host):
        self.host = host
        self.stations = ['46', '57', '148', '1723', '1747', '1752']

    def get_data(self, c_date=None, stations='all', sensors='pm10'):
        c_date = self._get_date(c_date)
        stations = self._get_stations(stations)
        r = self._build_request(
            c_date=c_date, stations=stations, sensors=sensors)
        return json.loads(r.content)

    def _get_date(self, c_date):
        r_date = datetime.now().strftime('%d.%m.%Y')
        if c_date:
            r_date = c_date
        return r_date

    def _get_stations(self, stations):
        r_stations = ''
        if stations == 'all':
            r_stations = '-'.join(self.stations)
        return r_stations

    def _build_request(self, c_date, stations, sensors):
        url = self.host + '/dane-pomiarowe/pobierz'
        # TO-DO: Check if headers are obligatory
        headers = self._build_headers(c_date, stations, sensors)
        params = self._build_params(c_date)
        return requests.post(url, data=params, headers=headers)

    def _build_headers(self, c_date, stations, sensors):
        bare_host = self.host.strip('http://')
        url = self.host + '/dane-pomiarowe/automatyczne'
        parameter = '/parametr/' + sensors
        stations = '/stations/' + stations
        date_range = '/dzienny/'

        sys_info = "(X11; Ubuntu; Linux x86_64; rv:43.0)"
        browsing_info = "Mozilla/5.0 %s Gecko/20100101 Firefox/43.0" % sys_info

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Length': 234,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': 1,
            'Host': bare_host,
            'Referer': ''.join([url, parameter, stations, date_range, c_date]),
            'User-Agent': browsing_info,
            'X-Requested-With': 'XMLHttpRequest',
        }
        return headers

    def _build_params(self, c_date):
        data = {
            'measType': 'Auto',
            'viewType': 'Parameter',
            'dateRange': 'Day',
            'date': c_date,
            'viewTypeEntityId': 'pm10',
            'channels': self.stations
        }
        params = {'query': json.dumps(data)}
        return params


class SmogDataPresenter(object):

    def __init__(self):
        self.data_fetcher = None

    def show_smog(self):
        host = sys.argv[1]
        self._set_data_fetcher(host)
        smog_data = self.data_fetcher.get_data()
        for item in smog_data['data']['series']:
            print item['label']
            for item2 in item['data']:
                print datetime.fromtimestamp(
                    int(item2[0])).strftime("%Y-%m-%d %H:%M"), item2[1]
            print ''

    def _set_data_fetcher(self, host):
        self.data_fetcher = SmogDataFetcher(host)

if __name__ == '__main__':
    SmogDataPresenter().show_smog()
