import asyncio

import pytest
from asynctest import MagicMock

from krakus.client import Wios


@pytest.fixture
def wios():
    return Wios()


@pytest.fixture
def response():
    class Response:
        def json(self):
            return b'[{"foo":"bar"}]'

    return Response()


@pytest.fixture
def request_mock(event_loop, response):
    request = asyncio.Future()
    request.set_result(response)
    return request


@pytest.fixture
def async_client(request_mock):
    client = MagicMock()
    client.post.return_value = request_mock
    return client


@pytest.fixture
def httpx_mock(mocker, event_loop, async_client):
    # Mock httpx.AsyncClient with a mock which returns a mock that will return
    # the client mock when entering the async context manager.
    # `mock` is just a stub, we pass then `async_client` to the mock returned
    # when httpx.AsyncClient async context manager is entered.
    mock = MagicMock()
    called_mock = MagicMock()
    called_mock.__aenter__.return_value = async_client
    mock.return_value = called_mock
    mocker.patch('httpx.AsyncClient', new=mock)
    return mock


@pytest.fixture
def wios_station_data():
    """
    Hardcoded response chunk from WIOS API. The date will be always fixed but this
    shouldn't be a problem for the tests. The data represent one station
    """

    return {
        'success': True,
        'data': {
            'charts': [],
            'title': 'Dane pomiarowe dla stacji Aleja Krasińskiego w dniu 01.09.2019 r.',
            'unitLabel': '&micro;g/m<sup>3</sup>',
            'series': [
                {
                    'label': 'Pył zawieszony PM10',
                    'measType': 'auto',
                    'paramLabel': 'Pył zawieszony PM10',
                    'paramId': 'pm10',
                    'paramCode': 'PM10',
                    'paramPostfix': '',
                    'aggType': 'A1h',
                    'ord': 7,
                    'interval': 3600,
                    'count': 24,
                    'retroCount': 2,
                    'startTime': 1567296000,
                    'extStartTime': 1567288800,
                    'coverageRate': 0.75,
                    'isAvgValid': True,
                    'thresholds': {
                        'at': None,
                        'it': None,
                        'tv': None,
                        'lv': None,
                        'atDecimals': 0,
                        'itDecimals': 0,
                        'tvDecimals': 0,
                        'lvDecimals': 0,
                    },
                    'data': [
                        ['1567288800', '60.1667'],
                        ['1567292400', '54.9286'],
                        ['1567296000', '53.3917'],
                        ['1567299600', '57.3314'],
                        ['1567303200', '63.1458'],
                        ['1567306800', '62.896'],
                        ['1567310400', '65.3877'],
                        ['1567314000', '69.7245'],
                        ['1567317600', '68.2974'],
                        ['1567321200', '58.4398'],
                        ['1567324800', '53.137'],
                        ['1567328400', '42.9997'],
                        ['1567332000', '39.6642'],
                        ['1567335600', '31.1638'],
                        ['1567339200', '24.0181'],
                        ['1567342800', '23.5054'],
                        ['1567346400', '23.3274'],
                        ['1567350000', '22.0646'],
                        ['1567353600', '26.0808'],
                        ['1567357200', '25.6539'],
                        ['1567360800', '28.0024'],
                        ['1567364400', '31.8496'],
                        ['1567368000', '36.9952'],
                        ['1567371600', '35.7723'],
                        ['1567375200', '36.6898'],
                        ['1567378800', '36.5334'],
                    ],
                    'avg': {'avg': '42.3363', 'min': '22.0646', 'max': '69.7245'},
                    'thresholdsForAvg': {
                        'avg': {
                            'at': 300,
                            'it': 200,
                            'tv': None,
                            'lv': 50,
                            'atDecimals': 0,
                            'itDecimals': 0,
                            'tvDecimals': 0,
                            'lvDecimals': 0,
                        },
                        'min': None,
                        'max': None,
                    },
                    'decimals': 0,
                    'unit': 'ug/m3',
                    'unitLabel': '&micro;g/m<sup>3</sup>',
                    'scaleMin': None,
                    'scaleMax': None,
                    'chartTooltipContent': '%y.# %ly o godz. %x',
                },
                {
                    'label': 'Pył zawieszony PM2.5',
                    'measType': 'auto',
                    'paramLabel': 'Pył zawieszony PM2.5',
                    'paramId': 'pm2.5',
                    'paramCode': 'PM2.5',
                    'paramPostfix': '',
                    'aggType': 'A1h',
                    'ord': 8,
                    'interval': 3600,
                    'count': 24,
                    'retroCount': 2,
                    'startTime': 1567296000,
                    'extStartTime': 1567288800,
                    'coverageRate': 0.75,
                    'isAvgValid': True,
                    'thresholds': {
                        'at': None,
                        'it': None,
                        'tv': None,
                        'lv': None,
                        'atDecimals': 0,
                        'itDecimals': 0,
                        'tvDecimals': 0,
                        'lvDecimals': 0,
                    },
                    'data': [
                        ['1567288800', '34.7557'],
                        ['1567292400', '33.4092'],
                        ['1567296000', '27.6051'],
                        ['1567299600', '29.703'],
                        ['1567303200', '32.8482'],
                        ['1567306800', '32.7387'],
                        ['1567310400', '34.1395'],
                        ['1567314000', '36.3603'],
                        ['1567317600', '35.4298'],
                        ['1567321200', '30.2264'],
                        ['1567324800', '26.4421'],
                        ['1567328400', '20.7251'],
                        ['1567332000', '19.1507'],
                        ['1567335600', '14.4717'],
                        ['1567339200', '10.4663'],
                        ['1567342800', '9.49035'],
                        ['1567346400', '9.59045'],
                        ['1567350000', '10.2025'],
                        ['1567353600', '11.6236'],
                        ['1567357200', '12.0699'],
                        ['1567360800', '13.4676'],
                        ['1567364400', '15.6108'],
                        ['1567368000', '17.2072'],
                        ['1567371600', '17.6064'],
                        ['1567375200', '18.2091'],
                        ['1567378800', '18.7091'],
                    ],
                    'avg': {'avg': '21.0039', 'min': '9.49035', 'max': '36.3603'},
                    'thresholdsForAvg': {'avg': None, 'min': None, 'max': None},
                    'decimals': 0,
                    'unit': 'ug/m3',
                    'unitLabel': '&micro;g/m<sup>3</sup>',
                    'scaleMin': None,
                    'scaleMax': None,
                    'chartTooltipContent': '%y.# %ly o godz. %x',
                },
            ],
            'dateFormat': 'H:00',
            'viewType': 'station',
            'messageItem': None,
        },
    }
