#!/usr/bin/python3
# This piece of shit                               #
# has been made by Cedric Bonhomme                 #
####################################################

import requests
import datetime
import statistics

NOISE_LIMIT = 40
WEATHER_NICE = 20

# Utilitarian
#########################


class Utils():

    def __init__(self):
        pass

    def date(self, timestamp):
        t = timestamp.split('+', 1)[0].replace("T", "")
        return datetime.datetime.strptime(t, "%Y-%m-%d%H:%M:%S").strftime("%Y/%m/%d-%H:%M:%S")

# Get data from Cisco Panda
# pre-configured infrastructure
#####################################


class Panda():

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

    def collect(self):
        car = []
        for cdr in self.response.json():
            for _, value in cdr['dps'].items():
                car.append(value)
        return car


class People(Panda):

    def people_count(self, start_time, end_time):
        self.query = {"m": "avg:placemeter.ped{host=6182}",
                      "start": start_time, "end": end_time}
        self.fetch()
        return sum(self.collect())


class Accident(Panda):

    def noise_level(self, start_time, end_time):
        self.query = {"start": start_time, "end": end_time, "m": "sum:bruitparif.laeq_1mn{host=*}"}
        self.fetch()
        level = statistics.mean(self.collect())
        return statistics.mean(self.collect()), level > NOISE_LIMIT

    def car_count(self, start_time, end_time):
        self.query = {"start": start_time, "end": end_time,
                      "m": "sum:24h-sum-zero:placemeter.vehicle{host=6188,class=*}"}
        self.fetch()
        return sum(self.collect())

    def bike_count(self, start_time, end_time):
        self.query = {"start": start_time, "end": end_time,
                      "m": "sum:24h-sum-zero:placemeter.bike{host=6188,class=*}"}
        self.fetch()
        return sum(self.collect())


class Weather(Panda):

    def temperature(self):
        self.query = {"start": "1h-ago", "m": "sum:breezometer.temp{host=*}"}
        self.fetch()
        return statistics.mean(self.collect())

    def fresh_air(self):
        self.query = {"start": "1h-ago", "m": "sum:breezometer.aqi{host=*}"}
        self.fetch()
        return statistics.mean(self.collect())

    def humidity(self):
        self.query = {"start": "1h-ago", "m": "sum:breezometer.rh{host=*}"}
        self.fetch()
        return statistics.mean(self.collect())

    def pression(self):
        self.query = {"start": "1h-ago", "m": "sum:breezometer.pressure{host=*}"}
        self.fetch()
        return statistics.mean(self.collect())

# Main
####################################
if __name__ == '__main__':

    people = People()
    accident = Accident()
    weather = Weather()
    utils = Utils()

    # People
    people_total = people.people_count(
        start_time=utils.date("2016-05-01T14:45:07+00:00"), end_time=utils.date("2016-05-01T15:00:07+00:00"))
    print('There has been %d persons on 2016/05/01 in Place de la Nation' % people_total)

    # Weather
    print('It is %s with %d°C' % ('cold' if weather.temperature()
                                  <= WEATHER_NICE else 'hot', weather.temperature()))
    print('Relative humidity is of about %d percent' % weather.humidity())

    # Accident
    (noise_level, is_noisy) = accident.noise_level(
        utils.date("2016-05-01T14:45:07+00:00"), utils.date("2016-05-01T15:00:07+00:00"))
    if is_noisy:
        print('It is %s out there! %d Db' % ('noisy' if is_noisy else 'calm', noise_level))

    print('There has been %d cars passing by Place de la Nation since the beginnning of the hackathon' %
          (accident.car_count("2016/12/09-18:00:00", "2016/12/11-23:59:59")))

    print('There has been %d bikes passing by Place de la Nation since the beginnning of the hackathon' %
          (accident.bike_count("2016/12/09-18:00:00", "2016/12/11-23:59:59")))

    print('Quality of air %d points' % weather.fresh_air())

    print('Atmospheric pressure %d Pa' % weather.pression())
