import time
import pandas as pd
from kafka import KafkaProducer
from json import dumps
import requests
import config


def kafka_producer():
    producer = KafkaProducer(bootstrap_servers=['54.196.246.52:9119'],  # change ip and port number here
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    rome = (41.9028, 12.4964)
    antarctica = (-82.8628, 135)
    cairo = (30.0444, 31.2357)

    location = [rome, antarctica, cairo]

    exclude = 'minutely,hourly,daily,alerts'
    APIkey = config.APIkey

    t_end = time.time() + 10 * 1  # Amount of time data is sent for in seconds
    while time.time() < t_end:
        df_stream = pd.DataFrame(columns=["Latitude", "Longitude", "Temperature", "Humidity", "Wind Speed", "Timestamp"])
        for city in location:
            URL = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units=imperial&exclude={}&appid={}'.format(city[0], city[1], exclude, APIkey)
            r = requests.get(url=URL)
            data = r.json()
            latitude = data['lat']
            longitude = data['lon']
            current_info = data['current']
            new_row = {
                "Latitude": latitude,
                "Longitude": longitude,
                "Temperature": current_info['temp'],
                "Humidity": current_info['humidity'],
                "Wind Speed": current_info['wind_speed'],
                "Timestamp": current_info['dt']
            }
            df_stream = df_stream._append(new_row, ignore_index=True)
            producer.send('StockData', value=df_stream.to_json())  # Add topic name here
    print("done producing")


kafka_producer()
