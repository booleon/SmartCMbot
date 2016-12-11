#!/usr/bin/python3

import requests
import dateutil
import datetime
import statistics

NOISE_LIMIT = 40
WEATHER_NICE = 20


class panda():

    def __init__(self):
        self.headers = {
            'x-tsapi-token': "ysL76v2ZQKZPofWZ",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "a6649846-07d9-ea05-7216-7a668e48dbff"
        }
        self.url = 'https://173.39.240.235:8444/api/query'
        self.query = ''
        self.response = ''

    def fetch(self):
        self.response = requests.request(
            "GET", self.url, headers=self.headers, params=self.query, verify='cisco.pem')

    # TODO: start_time useless (is end_time - 15min)
    def people_count(self, start_time, end_time):
        self.query = {"m": "avg:placemeter.ped{host=6182}",
                      "start": start_time, "end": end_time}
        self.fetch()
        return sum(self.collect())

    def collect(self):
        car = []
        for cdr in self.response.json():
            for _, value in cdr['dps'].items():
                car.append(value)
        return car

    def noise_level(self, start_time, end_time):
        self.query = {"start": start_time, "end": end_time, "m": "sum:bruitparif.laeq_1mn{host=*}"}
        self.fetch()
        level = statistics.mean(self.collect())
        return statistics.mean(self.collect()), level > NOISE_LIMIT

    def temperature(self):
        self.query = {"start": "1h-ago", "m": "sum:breezometer.temp{host=*}"}
        self.fetch()
        return statistics.mean(self.collect())

if __name__ == '__main__':

    # Python is a shit language, it does not even pointers
    panda = panda()

    # Please fix this joke of a language TODO: Date is a date
    people_total = panda.people_count(
        start_time="2016/05/01-14:45:00", end_time="2016/05/01-15:00:00")
    print('There has been %d persons on 2016/05/01 in Place de la Nation' % people_total)

    ####################NOISE#################################################
    (noise_level, is_noisy) = panda.noise_level("2016/05/01-14:45:00", "2016/05/01-15:00:00")
    if is_noisy:
        print('It is noisy out there! %d Db' % noise_level)
    ##########################################################################

    print('It is %s with %d°C' % ('cold' if panda.temperature()
                                  <= WEATHER_NICE else 'hot', panda.temperature()))
