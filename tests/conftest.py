import pytest

from krakus.client import Wios


@pytest.fixture
def krakus():
    return Wios()
