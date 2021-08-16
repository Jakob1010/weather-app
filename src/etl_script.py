from datetime import datetime
from collections import Counter
from typing import Any, Dict, List, Optional
import psycopg2.extras as p
from utils.constants import get_weather_api_key
from utils.openweather_utils import get_cities_list, get_openweather_baseUrl
import requests
import json
import sys

from utils.db import WarehouseConnection
from utils.sde_config import get_warehouse_creds


def pull_weather_date() -> List[Dict[str, Any]]:
    print('>>pull weather data')

    # construct url 
    apiKey = get_weather_api_key()
    cities = get_cities_list()
    citieIds = ','.join(cities.keys())
    url = get_openweather_baseUrl().format(cities=citieIds,api_key=apiKey)
    try:
        response = requests.get(url)
    except requests.ConnectionError as ce:
        print(f"--Pull weather request failed, {ce}")
        sys.exit(1)
    
    data = json.loads(response.text)
    dt = datetime.today().strftime('%Y-%m-%d')
    print('main',data["list"])
    for item in data["list"]:
        id = str(item["id"])
        temp = item["main"]["temp"]
        cities[id]["dt"] = dt
        cities[id]["avg_temperature"] = temp

    return cities.values()


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

def insert_data(weather:List[Dict[str, Any]]):
    print('>>insert data')
    print(weather)
    try:
        with WarehouseConnection(**get_warehouse_creds()).managed_cursor_etl() as curr:
            p.execute_batch(curr, get_insert_query(), weather)
            print('++insert success!')
    except Exception as e:
        print(f"--Insert data failed, {e}")

def run() -> None:
    weather_data = pull_weather_date()
    insert_data(weather_data)    


if __name__ == '__main__':
    run()
