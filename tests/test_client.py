import pytest

from krakus.exceptions import InvalidDateFormat, InvalidDateRange


def test_date_range_valid(krakus):
    krakus._validate_date_range('2000-01-01', '2000-01-20')


def test_date_range_invalid(krakus):
    with pytest.raises(InvalidDateRange):
        krakus._validate_date_range('2000-01-01', '1999-12-20')


@pytest.mark.parametrize('input_date,expected', [('2045-11-01', '01.11.2045'), ('2013-04-28', '28.04.2013')])
def test_wios_date_format(krakus, input_date, expected):
    assert krakus._format_date_wios(input_date) == expected


def test_format_invalid_date(krakus):
    with pytest.raises(InvalidDateFormat):
        krakus._format_date_wios('0-76-45')
