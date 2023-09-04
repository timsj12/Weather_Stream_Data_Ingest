import json
import requests
import time

rome = (41.9028, 12.4964)
antarctica = (-82.8628, 135)
cairo = (30.0444, 31.2357)

location = [rome, antarctica, cairo]

exclude = 'minutely,hourly,daily,alerts'
APIkey = '2f87882d231da0d6cead66fa10196364'

for city in location:
    URL = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units=imperial&exclude={}&appid={}'.format(city[0], city[1], exclude, APIkey)
    r = requests.get(url=URL)
    data = r.json()

    print(data)
