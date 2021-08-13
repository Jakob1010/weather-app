import os
from typing import Dict, Optional, Union


def get_warehouse_creds() -> Dict[str, Optional[Union[str, int]]]:
    return {
        'user': 'jakob',
        'password': 'password',
        'db': 'temperature_db',
        'host': 'localhost',
        'port': 5432
    }