import asyncio
from datetime import date, timedelta

import httpx

from .structures import STATION_MAP
from .exceptions import InvalidDateRange
from .types import IsoDate


class Krakus:
    """
    Get data from http://monitoring.krakow.pios.gov.pl API
    """
    url = 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/pobierz'
    query = '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"%s","viewTypeEntityId":"%s","channels":[%s]}'

    def _validate_date_range(self, start, end):
        if start > end:
            raise InvalidDateRange()

    async def get(self, date: IsoDate) -> list:
        async with httpx.AsyncClient() as client:
            date_components = date.split('-')
            new_date = f'{date_components[2]}.{date_components[1]}.{date_components[0]}'
            queries = [
                self.query % (new_date, station.id, f'{station.pm10_code},{station.pm25_code}') if station.pm25_code else self.query % (
                    new_date, station.id, station.pm10_code)
                for station in STATION_MAP.values()
            ]
            tasks = [client.post(self.url, data={'query': query}) for query in queries]
            res = await asyncio.gather(*tasks)
            return [r.content for r in res]

    async def get_range(self, start_range: IsoDate, end_range: IsoDate):
        start = date.fromisoformat(start_range)
        end = date.fromisoformat(end_range)
        self._validate_date_range(start, end)
        tasks = []
        while start < end:
            tasks.append(self.get(start.isoformat()))
            start = start + timedelta(days=1)

        return await asyncio.gather(*tasks)
