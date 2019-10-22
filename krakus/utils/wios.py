import re

STATION_REGEX = re.compile(r'Dane pomiarowe dla stacji\s(.*) w dniu ([0-9]+.[0-9]+.[0-9]+).*')


class StationDataInterface:
    """
    Main interface for station data gathered by the WIOS API.
    Every instance will represent a single station, so if you have more
    than one station in the API response, you should instantiate this class
    multiple times.
    """

    def __init__(self, station_data):
        self._station_data = station_data

    @property
    def data(self) -> dict:
        return self._station_data['data']

    @property
    def name(self) -> str:
        match = STATION_REGEX.search(self.title)
        if match:
            return match.group(1)
        else:
            return ''

    @property
    def date(self) -> str:
        match = STATION_REGEX.search(self.title)
        if match:
            return match.group(2)
        else:
            return ''

    @property
    def title(self) -> str:
        return self.data['title']

    @property
    def series(self) -> list:
        return self.data['series']

    def _filter_series(self, key: str) -> list:
        try:
            pm_readings = next(filter(lambda x: x['paramId'] == key, self.series))
            return pm_readings['data']
        except StopIteration:
            return []

    @property
    def pm10_data(self) -> list:
        return self._filter_series('pm10')

    @property
    def pm25_data(self) -> list:
        return self._filter_series('pm2.5')
