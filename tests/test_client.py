import os

import pytest
from dotenv import load_dotenv

from pygourmet import Api
from pygourmet.client import SearchError
from pygourmet.option import Option

load_dotenv()
HOTPEPPER_KEYID = os.getenv("HOTPEPPER_KEYID", None)


@pytest.mark.integration
@pytest.mark.skipif(HOTPEPPER_KEYID is None, reason="HOTPEPPER_KEYID is not set")
def test_search_optionなし():
    """本番APIを使用したテスト（通常はスキップされる）"""
    assert HOTPEPPER_KEYID is not None
    client = Api(HOTPEPPER_KEYID)
    option = Option()
    with pytest.raises(SearchError) as e:
        _ = client.search(option)

    assert (
        str(e.value) == "パラメータ不正エラー: 少なくとも１つの条件を入れてください。"
    )


@pytest.mark.integration
@pytest.mark.skipif(HOTPEPPER_KEYID is None, reason="HOTPEPPER_KEYID is not set")
def test_search_位置指定():
    """本番APIを使用したテスト（通常はスキップされる）"""
    assert HOTPEPPER_KEYID is not None
    client = Api(HOTPEPPER_KEYID)
    lat, lng = 34.8586318, 136.8139928
    option = Option(lat=lat, lng=lng)
    shops = client.search(option)

    assert len(shops) > 0
    for shop in shops:
        # NOTE 初期設定は1000m以内
        assert shop.meters_to_point(lat=lat, lng=lng) <= 1000
