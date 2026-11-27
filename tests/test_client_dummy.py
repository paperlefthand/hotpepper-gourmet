import json
import os

import pytest
from pydantic import ValidationError

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


def test_search_dummy_results欠落(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"unexpected": {}})

    with pytest.raises(SearchError) as e:
        _ = client_dummy.search(Option(keyword="ラーメン"))

    assert isinstance(e.value.__cause__, KeyError)


def test_search_dummy_shopパース失敗(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": [{"lat": "not-a-number"}]}})

    with pytest.raises(SearchError) as e:
        _ = client_dummy.search(Option(keyword="ラーメン"))

    assert isinstance(e.value.__cause__, ValidationError)


@pytest.mark.asyncio
async def test_search_async_dummy_shopパース失敗(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": [{"lat": "not-a-number"}]}})

    with pytest.raises(SearchError) as e:
        _ = await client_dummy.search_async(Option(keyword="ラーメン"))

    assert isinstance(e.value.__cause__, ValidationError)


def _load_resp(filename):
    with open(os.path.join(DATAFILE_PATH, filename), "r", encoding="utf-8") as f:
        return json.load(f)


def _assert_特集とクレジットカード(shops, mock_response):
    expected = mock_response["results"]["shop"][0]
    shop = shops[0]
    assert shop.special is not None
    assert len(shop.special) == len(expected["special"])
    assert shop.special[0].code == expected["special"][0]["code"]
    assert shop.special[0].title == expected["special"][0]["title"]
    assert shop.special[0].special_category is not None
    assert (
        shop.special[0].special_category.code
        == expected["special"][0]["special_category"]["code"]
    )
    assert shop.credit_card is not None
    assert [c.code for c in shop.credit_card] == [
        c["code"] for c in expected["credit_card"]
    ]


def test_search_dummy_特集とクレジットカード(client_dummy, httpx_mock):
    mock_response = _load_resp("restaurant_resp_3.json")
    httpx_mock.add_response(json=mock_response)

    shops = client_dummy.search(Option(large_area="Z011", type="credit_card+special"))

    assert httpx_mock.get_request().url.params["type"] == "credit_card+special"
    _assert_特集とクレジットカード(shops, mock_response)


@pytest.mark.asyncio
async def test_search_async_dummy_特集とクレジットカード(client_dummy, httpx_mock):
    mock_response = _load_resp("restaurant_resp_3.json")
    httpx_mock.add_response(json=mock_response)

    shops = await client_dummy.search_async(
        Option(large_area="Z011", type="credit_card+special")
    )

    _assert_特集とクレジットカード(shops, mock_response)


def test_search_dummy_特集とクレジットカードなし(client_dummy, httpx_mock):
    with open(
        os.path.join(DATAFILE_PATH, "restaurant_resp_0.json"), "r", encoding="utf-8"
    ) as f:
        mock_response = json.load(f)
    httpx_mock.add_response(json=mock_response)

    shops = client_dummy.search(Option(keyword="ラーメン"))

    # type 未指定のレスポンスには含まれない
    assert all(shop.special is None and shop.credit_card is None for shop in shops)
