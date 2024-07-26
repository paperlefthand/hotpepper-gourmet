import json
import os

import pytest

from pygourmet.client import Api
from pygourmet.option import Option

DATAFILE_PATH = os.path.join(os.path.dirname(__file__), "data")
BASE_URL = Api.BASE_URL


def test_search_optionなし(client, httpx_mock):
    with open(
        os.path.join(DATAFILE_PATH, "restaurant_resp_0.json"), "r", encoding="utf-8"
    ) as f:
        mock_response = json.load(f)

    httpx_mock.add_response(json=mock_response)

    option = Option()  # type: ignore
    shops = client.search(option)
    assert shops == mock_response["results"]["shop"]


def test_search_optionあり(client, httpx_mock):
    with open(
        os.path.join(DATAFILE_PATH, "restaurant_resp_0.json"), "r", encoding="utf-8"
    ) as f:
        mock_response = json.load(f)

    httpx_mock.add_response(json=mock_response)

    option = Option(keyword="ラーメン", lat=35.0, lng=135.0, radius=3000)  # type: ignore
    shops = client.search(option)
    assert shops == mock_response["results"]["shop"]


@pytest.mark.asyncio
async def test_async_search_optionなし(client, httpx_mock):
    with open(
        os.path.join(DATAFILE_PATH, "restaurant_resp_0.json"), "r", encoding="utf-8"
    ) as f:
        mock_response = json.load(f)

    httpx_mock.add_response(json=mock_response)

    option = Option()  # type: ignore
    shops = await client.async_search(option)
    assert shops == mock_response["results"]["shop"]
