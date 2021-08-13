import datetime
from collections import Counter
from typing import Any, Dict, List, Optional
import psycopg2.extras as p

from utils.db import WarehouseConnection
from utils.sde_config import get_warehouse_creds

def get_insert_query() -> str:
    return '''
        INSERT INTO words_reddit(
            word,
            post_title,
            subreddit,
            score,
            post_url,
            post_utc
        )
        VALUES (
            %(word)s,
            %(title)s,
            %(subreddit)s,
            %(score)s,
            %(url)s,
            %(time)s
        );
    '''


def run() -> None:
    try: 
        with WarehouseConnection(**get_warehouse_creds()).managed_cursor() as curr:
            p.execute_batch(curr, get_insert_query())
    except Exception as e:
        print(e)
        
    

if __name__ == '__main__':
    run()
