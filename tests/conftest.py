import pytest

from krakus.client import Krakus


@pytest.fixture
def krakus():
    return Krakus()
