import json
import os

import pytest

from pygourmet.client import SearchError
from pygourmet.option import Option

DATAFILE_PATH = os.path.join(os.path.dirname(__file__), "data")


def test_search_dummy_optionなし(client_dummy, httpx_mock):
    option = Option()
    httpx_mock.add_response(
        json={
            "results": {
                "api_version": "1.30",
                "error": [
                    {"code": 3000, "message": "少なくとも１つの条件を入れてください。"}
                ],
            }
        }
    )
    with pytest.raises(SearchError) as e:
        _ = client_dummy.search(option)

    assert len(httpx_mock.get_requests()) == 1
    assert (
        str(e.value) == "パラメータ不正エラー: 少なくとも１つの条件を入れてください。"
    )


def test_search_dummy_optionあり(client_dummy, httpx_mock):
    with open(
        os.path.join(DATAFILE_PATH, "restaurant_resp_0.json"), "r", encoding="utf-8"
    ) as f:
        mock_response = json.load(f)

    httpx_mock.add_response(json=mock_response)

    option = Option(keyword="ラーメン", lat=35.0, lng=135.0, range=3)
    shops = client_dummy.search(option)
    for i, shop in enumerate(shops):
        assert shop.name == mock_response["results"]["shop"][i]["name"]


@pytest.mark.asyncio
async def test_search_async_dummy_optionなし(client_dummy, httpx_mock):
    option = Option()
    httpx_mock.add_response(
        json={
            "results": {
                "api_version": "1.30",
                "error": [
                    {"code": 3000, "message": "少なくとも１つの条件を入れてください。"}
                ],
            }
        }
    )
    with pytest.raises(SearchError) as e:
        _ = await client_dummy.search_async(option)

    assert len(httpx_mock.get_requests()) == 1
    assert (
        str(e.value) == "パラメータ不正エラー: 少なくとも１つの条件を入れてください。"
    )
