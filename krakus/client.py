import asyncio
from datetime import date as dt
from datetime import timedelta
from typing import List

import httpx

from .exceptions import InvalidDateFormat, InvalidDateRange
from .structures import STATION_MAP
from .types import IsoDate, WiosDate


class Wios:
    """
    Get data from http://monitoring.krakow.pios.gov.pl API
    """

    url = 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/pobierz'
    query = '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"%s","viewTypeEntityId":"%s","channels":[%s]}'

    def _validate_date_range(self, start, end) -> None:
        if start > end:
            raise InvalidDateRange()

    def _format_date_wios(self, date: IsoDate) -> WiosDate:
        try:
            dt.fromisoformat(date)
        except ValueError:
            raise InvalidDateFormat()

        date_components = date.split('-')
        return WiosDate(f'{date_components[2]}.{date_components[1]}.{date_components[0]}')

    def _build_query(self, date: IsoDate) -> List[str]:
        new_date = self._format_date_wios(date)
        queries = []
        for station in STATION_MAP.values():
            if station.pm25_code:
                queries.append(self.query % (new_date, station.id, f'{station.pm10_code},{station.pm25_code}'))
            else:
                queries.append(self.query % (new_date, station.id, station.pm10_code))

        return queries

    async def get(self, date: IsoDate) -> List[str]:
        """
        Given a date in format YYYY-MM-DD, gets the pollution data for all WIOS stations in Krakow
        """
        async with httpx.AsyncClient() as client:
            queries = self._build_query(date)
            tasks = [client.post(self.url, data={'query': query}) for query in queries]
            res = await asyncio.gather(*tasks)
            return [r.content for r in res]

    async def get_range(self, start_range: IsoDate, end_range: IsoDate):
        start = dt.fromisoformat(start_range)
        end = dt.fromisoformat(end_range)
        self._validate_date_range(start, end)
        tasks = []
        while start < end:
            tasks.append(self.get(IsoDate(start.isoformat())))
            start = start + timedelta(days=1)

        return await asyncio.gather(*tasks)
