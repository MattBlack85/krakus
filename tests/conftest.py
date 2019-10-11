import asyncio

import pytest
from asynctest import CoroutineMock, MagicMock

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
