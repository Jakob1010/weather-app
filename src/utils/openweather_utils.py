from typing import Any, Dict, Optional, Union, List


def get_openweather_baseUrl() -> str:
    # placeholder1: ids of cites; placeholder2: apiKey
    return 'https://api.openweathermap.org/data/2.5/group?id={cities}&units=metric&appid={api_key}'


def get_cities_list() -> Dict[str,Dict[str, Any]]:
    return {
        "2761369": {"region": "Europe", "country": "Austria", "city": "Vienna"},
        "1819729": {"region": "Asia", "country": "Hong Kong", "city": "Hong Kong"},
        "524901": {"region": "Europe", "country": "Russia", "city": "Moscow"},
    }
