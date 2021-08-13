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
    df = pd.read_csv('../res/city_temperature.csv',low_memory=False)

    # filter outliner
    df = df[df['AvgTemperature']>-70]

    # sort by date
    df.sort_values(['Year', 'Month', 'Day'])

    # combine Year, Month, Day column to Date column
    df['Date'] = pd.to_datetime((df.Year*10000+df.Month*100+df.Day).apply(str),format='%Y%m%d')

    # filter columns
    df = df.loc[0:2899539,['Region','Country','City', 'Date', 'AvgTemperature']]
    df.columns = ['region', 'country', 'city', 'dt', 'avg_temperature']
    print(df.head(5))

    return df

def insert_data(temperature_data:pd.DataFrame):
    print('>>insert_temp_data')
    try: 
        connect_url = 'postgresql+psycopg2://jakob:password@localhost:5432/temperature_db'
        engine = create_engine(connect_url)
        conn = engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()
        temperature_data.to_csv(output, sep='\t', header=False, index=True)
        output.seek(0)
        contents = output.getvalue()
        cur.copy_from(output, 'temperature', null="") # null values become ''
        conn.commit()
        print('>>insert_temp_data: success!')
    except Exception as e:
        print(e)
        print('>>insert_temp_data: error!')


if __name__ == '__main__':
    temp = get_csv_temp()
    insert_data(temp)