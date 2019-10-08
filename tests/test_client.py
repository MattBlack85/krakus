import pytest

from krakus.client import Krakus
from krakus.exceptions import InvalidDateRange


def test_date_range_valid():
    k = Krakus()
    k._validate_date_range('2000-01-01', '2000-01-20')


def test_date_range_invalid():
    k = Krakus()
    with pytest.raises(InvalidDateRange):
        k._validate_date_range('2000-01-01', '1999-12-20')
