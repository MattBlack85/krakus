import pytest

from krakus.client import Wios


@pytest.fixture
def wios():
    return Wios()
