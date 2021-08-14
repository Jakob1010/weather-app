import numpy as np
import pandas as pd
from sqlalchemy import create_engine, engine
import psycopg2
import io
from utils.db import WarehouseConnection
from utils.sde_config import get_warehouse_creds


def get_csv_temp() -> pd.DataFrame:
    print('>>get_csv_temp')
    # read csv file from res
    df = pd.read_csv('../res/city_temperature.csv', low_memory=False)

    # filter outliner
    df = df[df['AvgTemperature'] > -70]

    # sort by date
    df.sort_values(['Year', 'Month', 'Day'])

    # combine Year, Month, Day column to Date column
    df['Date'] = pd.to_datetime(
        (df.Year*10000+df.Month*100+df.Day).apply(str), format='%Y%m%d')

    # filter columns
    df = df.loc[0:2899539, ['Region', 'Country',
                            'City', 'Date', 'AvgTemperature']]
    df.columns = ['region', 'country', 'city', 'dt', 'avg_temperature']

    # convert temperature
    df['avg_temperature'] = df['avg_temperature'].apply(fahrenheit_to_celsius)

    print(df.head(5))
    return df


def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9


def insert_data(temperature_data: pd.DataFrame):
    print('>>insert_temp_data')
    try:
        with WarehouseConnection(**get_warehouse_creds()).managed_cursor() as curr:
            output = io.StringIO()
            temperature_data.to_csv(output, sep='\t', header=False, index=True)
            output.seek(0)
            contents = output.getvalue()
            # null values become ''
            curr.copy_from(output, 'temperature', null="")
            #curr.execute('ALTER TABLE temperature ADD PRIMARY KEY (index);')
            #curr.execute('ALTER TABLE temperature CHANGE index id INT( 11 ) NOT NULL AUTO_INCREMENT')
            print('>>insert_temp_data: success!')
    except Exception as e:
        print('>>insert_temp_data: error!')
        print(e)


if __name__ == '__main__':
    temp = get_csv_temp()
    insert_data(temp)
