import pytest

from krakus.exceptions import InvalidDateFormat, InvalidDateRange


def test_date_range_valid(wios):
    wios._validate_date_range('2000-01-01', '2000-01-20')


def test_date_range_invalid(wios):
    with pytest.raises(InvalidDateRange):
        wios._validate_date_range('2000-01-01', '1999-12-20')


@pytest.mark.parametrize('input_date,expected', [('2045-11-01', '01.11.2045'), ('2013-04-28', '28.04.2013')])
def test_wios_date_format(wios, input_date, expected):
    assert wios._format_date_wios(input_date) == expected


def test_format_invalid_date(wios):
    with pytest.raises(InvalidDateFormat):
        wios._format_date_wios('0-76-45')


def test_query_building(wios):
    expected = [
        '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"01.01.2019","viewTypeEntityId":"161","channels":[1921]}',
        '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"01.01.2019","viewTypeEntityId":"152","channels":[1747]}',
        '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"01.01.2019","viewTypeEntityId":"6","channels":[46,202]}',
        '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"01.01.2019","viewTypeEntityId":"173","channels":[2176]}',
        '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"01.01.2019","viewTypeEntityId":"153","channels":[1752]}',
        '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"01.01.2019","viewTypeEntityId":"16","channels":[148,242]}',
        '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"01.01.2019","viewTypeEntityId":"149","channels":[1723]}',
    ]

    assert wios._build_query('2019-01-01') == expected


@pytest.mark.asyncio
async def test_get_data_for_single_day(wios, httpx_mock, async_client, mocker):
    mocker.patch.object(wios, '_build_query', return_value=[b'foo', b'foo', b'foo'])
    res = await wios.get('2019-01-01')
    assert len(res) == 3
    assert async_client.post.call_count == 3
    wios._build_query.assert_called_once_with('2019-01-01')
