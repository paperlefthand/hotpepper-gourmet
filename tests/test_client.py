import os

import pytest
from dotenv import load_dotenv

from pygourmet import Api
from pygourmet.client import SearchError
from pygourmet.option import Option

load_dotenv()
is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(is_github_actions, reason="CI環境ではスキップ")
def test_search_optionなし():
    client = Api(os.environ["HOTPEPPER_KEYID"])
    option = Option()
    with pytest.raises(SearchError) as e:
        _ = client.search(option)

    assert (
        str(e.value) == "パラメータ不正エラー: 少なくとも１つの条件を入れてください。"
    )


@pytest.mark.skipif(is_github_actions, reason="CI環境ではスキップ")
def test_search_位置指定():
    client = Api(os.environ["HOTPEPPER_KEYID"])
    lat, lng = 34.8586318, 136.8139928
    option = Option(lat=lat, lng=lng)
    shops = client.search(option)

    assert len(shops) > 0
    for shop in shops:
        # NOTE 初期設定は1000m以内
        assert shop.meters_to_point(lat=lat, lng=lng) <= 1000
