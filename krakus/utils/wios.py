import csv
import pathlib
import re

from .date import convert_ts_to_dt

STATION_REGEX = re.compile(r'Dane pomiarowe dla stacji\s(.*) w dniu ([0-9]+.[0-9]+.[0-9]+).*')
HERE = pathlib.Path(__file__).parents[0]


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
            raw_data = pm_readings['data']
            return {element[0]: element[1] for element in raw_data}
        except StopIteration:
            return {}

    @property
    def pm10_data(self) -> list:
        return self._filter_series('pm10')

    @property
    def pm25_data(self) -> list:
        return self._filter_series('pm2.5')


def dump_wios_data_to_csv(data: dict) -> None:
    with (HERE / '../../data/wios.csv').open('w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        rows_to_dump = []

        for station in data:
            station = StationDataInterface(station)

            # No data at all
            if not station.pm10_data and not station.pm25_data:
                continue

            # Just PM10 data
            elif station.pm10_data and not station.pm25_data:
                for time, measurement in station.pm10_data.items():
                    dt = convert_ts_to_dt(time)
                    base_row = [
                        # title
                        station.name,
                        # year
                        dt.year,
                        # month
                        dt.month,
                        # day
                        dt.day,
                        # hour
                        dt.hour,
                        # PM10
                        measurement,
                        # PM2.5
                        None,
                    ]
                    rows_to_dump.append(base_row)

            # Just PM2.5 data
            elif not station.pm10_data and station.pm25_data:
                for time, measurement in station.pm25_data.items():
                    dt = convert_ts_to_dt(time)
                    base_row = [
                        # title
                        station.name,
                        # year
                        dt.year,
                        # month
                        dt.month,
                        # day
                        dt.day,
                        # hour
                        dt.hour,
                        # PM10
                        None,
                        # PM2.5
                        measurement,
                    ]
                    rows_to_dump.append(base_row)

            # Both PM10 and PM2.5 data
            else:
                for time, measurement in station.pm10_data.items():
                    dt = convert_ts_to_dt(time)
                    base_row = [
                        # title
                        station.name,
                        # year
                        dt.year,
                        # month
                        dt.month,
                        # day
                        dt.day,
                        # hour
                        dt.hour,
                        # PM10
                        measurement,
                    ]
                    # check if there is a match for the same time for PM2.5
                    if time in station.pm25_data:
                        base_row.append(station.pm25_data[time])
                    else:
                        base_row.append(None)

                    rows_to_dump.append(base_row)

                # Make a double check o find if there was any time in PM2.5 that hadn't
                # a match in PM10 time series+3
                for time, measurement in station.pm25_data.items():
                    if time not in station.pm10_data:
                        rows_to_dump.append(
                            [
                                # title
                                station.name,
                                # year
                                dt.year,
                                # month
                                dt.month,
                                # day
                                dt.day,
                                # hour
                                dt.hour,
                                # PM10
                                None,
                                # PM25
                                measurement,
                            ]
                        )

        writer.writerows(rows_to_dump)
