import asyncio
from collections import namedtuple

import httpx

Station = namedtuple('Station', ['id', 'pm10_code', 'pm25_code'], defaults=[None])
pm_map = {
    'os. Wadów': Station(id='161', pm10_code='1921'),
    'os. Piastów': Station(id='152', pm10_code='1747'),
    'Aleja Krasińskiego': Station(id='6', pm10_code='46', pm25_code='202'),
    'os. Swoszowice': Station(id='173', pm10_code='2176'),
    'ul. Złoty Róg': Station(id='153', pm10_code='1752'),
    'Kurdwanów': Station(id='16', pm10_code='148', pm25_code='242'),
    'ul. Dietla': Station(id='149', pm10_code='1723'),
}


class Krakus:
    """
    Get data from http://monitoring.krakow.pios.gov.pl API
    """
    url = 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/pobierz'
    query = '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"%s","viewTypeEntityId":"%s","channels":[%s]}'

    async def get(self, date: str) -> list:
        async with httpx.AsyncClient() as client:
            queries = [
                self.query % (date, station.id, f'{station.pm10_code},{station.pm25_code}') if station.pm25_code else self.query % (
                    date, station.id, station.pm10_code)
                for station in pm_map.values()
            ]
            tasks = [client.post(self.url, data={'query': query}) for query in queries]
            return await asyncio.gather(*tasks)
