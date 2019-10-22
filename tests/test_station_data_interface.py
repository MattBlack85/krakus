from datetime import datetime

import pytest

from krakus.utils.wios import STATION_REGEX, StationDataInterface


def test_title(wios_station_data):
    interface = StationDataInterface(wios_station_data)
    assert interface.title == wios_station_data['data']['title']
    assert isinstance(interface.title, str)


def test_data(wios_station_data):
    interface = StationDataInterface(wios_station_data)
    assert interface.data == wios_station_data['data']
    assert isinstance(interface.data, dict)


def test_series(wios_station_data):
    interface = StationDataInterface(wios_station_data)
    assert interface.series == wios_station_data['data']['series']
    assert isinstance(interface.series, list)


def test_filter_with_empty_series(wios_station_data):
    wios_station_data['data']['series'] = []
    interface = StationDataInterface(wios_station_data)
    assert interface._filter_series('pm10') == []


def test_filter_bad_key(wios_station_data):
    interface = StationDataInterface(wios_station_data)
    assert interface._filter_series('foo') == []


@pytest.mark.parametrize('attr', ['pm10_data', 'pm25_data'])
def test_pm_data(attr, wios_station_data):
    interface = StationDataInterface(wios_station_data)
    # for some reasons there are 26 measurements for one single day
    assert len(getattr(interface, attr)) == 26
    for element in getattr(interface, attr):
        assert isinstance(element, list)
        # First element is a str represeting a unix timestamp,
        # this will make sure we can convert it
        datetime.fromtimestamp(int(element[0]))
        # The second element is a str representing a float, this
        # will make sure we are dealing with such a thing.
        float(element[1])


@pytest.mark.parametrize(
    'test_string,expected_name',
    [
        ('Dane pomiarowe dla stacji Aleja Krasińskiego w dniu 01.09.2019 r.', 'Aleja Krasińskiego'),
        ('Dane pomiarowe dla stacji Kraków-Kurdwanów w dniu 01.09.2019 r.', 'Kraków-Kurdwanów'),
        ('Dane pomiarowe dla stacji Kraków, ul. Złoty Róg w dniu 01.09.2019 r.', 'Kraków, ul. Złoty Róg'),
    ],
)
def test_station_regex(test_string, expected_name):
    match = STATION_REGEX.search(test_string)
    assert match is not None
    assert match.group(2) == '01.09.2019'
    assert match.group(1) == expected_name


def test_name(wios_station_data):
    interface = StationDataInterface(wios_station_data)
    assert interface.name == 'Aleja Krasińskiego'


def test_empty_name(wios_station_data):
    wios_station_data['data']['title'] = ''
    interface = StationDataInterface(wios_station_data)
    assert interface.name == ''


def test_date(wios_station_data):
    interface = StationDataInterface(wios_station_data)
    assert interface.date == '01.09.2019'


def test_empty_date(wios_station_data):
    wios_station_data['data']['title'] = ''
    interface = StationDataInterface(wios_station_data)
    assert interface.date == ''
