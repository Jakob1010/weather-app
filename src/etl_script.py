import datetime
from collections import Counter
from typing import Any, Dict, List, Optional
import psycopg2.extras as p
from utils.constants import get_weather_api_key
import requests
import json

from utils.db import WarehouseConnection
from utils.sde_config import get_warehouse_creds


def pull_weather_date() -> List:
    print('>>pull weather data')
    str_url = 'https://api.openweathermap.org/data/2.5/weather?q=London,uk&units=metric&appid='
    str_url = str_url + get_weather_api_key()
    print(str_url)
    response = requests.get(str_url)
    data = json.loads(response.text)
    return List


def get_insert_query() -> str:
    return '''
        INSERT INTO temperature(
            region,
            country,
            city,
            dt,
            avg_temperature
        )
        VALUES (
            %(region)s,
            %(country)s,
            %(city)s,
            %(dt)s,
            %(avg_temperature)s
        );
    '''


def run() -> None:
    pull_weather_date()
    #try:
    #    with WarehouseConnection(**get_warehouse_creds()).managed_cursor() as curr:
    #        p.execute_batch(curr, get_insert_query())
    #except Exception as e:
    #    print(e)


if __name__ == '__main__':
    run()
