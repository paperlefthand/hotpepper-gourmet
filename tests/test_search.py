from pytest import raises

from pygourmet.errors import PyGourmetError

# def test_search(api):
#     with requests_mock.Mocker() as m:
#         m.get(
#             Api.BASE_URL,
#             json={"results": {"shop": []}},
#         )
#         result = api.search(35.681236, 139.767125)
#         assert result == {"results": {"shop": []}}


# def test_search_restaurants_set_keyword(api):
#     result = api.search(lat=35.170915, lng=136.8793482, radius=400, keyword="ラーメン")
#     assert len(result) > 1, "キーワードに合致する店が取得できる"


# def test_search_restaurants_default_count(api):
#     result = api.search(lat=35.170915, lng=136.8793482, radius=400)
#     assert len(result) == 10, "件数を指定しなければ最大10件出力される"


# def test_search_restaurants_5_count(api):
#     result = api.search(lat=35.170915, lng=136.8793482, count=5)
#     assert len(result) == 5, "指定した件数通りに取得できる"


def test_search_restaurants_minus_count(api):
    with raises(PyGourmetError) as e:
        _ = api.search(lat=35.170915, lng=136.8793482, count=-1)

    assert (
        str(e.value) == "Invalid count value (must be >= 0)"
    ), "件数に負の値を入れるとエラー"


def test_search_restaurants_minus_radius(api):
    with raises(PyGourmetError) as e:
        _ = api.search(lat=35.170915, lng=136.8793482, radius=-1)

    assert (
        str(e.value) == "Invalid radius value (must be >= 0)"
    ), "範囲に負の値を入れるとエラー"


# @responses.activate
# def test_search_restaurant(api, helpers):
#     restaurant_data = helpers.load_json_data("tests/data/restaurant_resp.json")

#     responses.add(responses.GET, url=api.BASE_URL, json=restaurant_data)
#     resp = api.search(lat=35.170915, lng=136.8793482, radius=1000, count=1)

#     assert resp[0]["lat"] == 35.6933654897, "座標が正しく取り出せること"
#     assert resp[0]["lat"] == 35.6933654897, "座標が正しく取り出せること"
