import pytest


from krakus.exceptions import InvalidDateRange


def test_date_range_valid(krakus):
    krakus._validate_date_range('2000-01-01', '2000-01-20')


def test_date_range_invalid(krakus):
    with pytest.raises(InvalidDateRange):
        krakus._validate_date_range('2000-01-01', '1999-12-20')
