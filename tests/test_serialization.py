import pytest
from pydantic import ValidationError

from pygourmet.option import Option


def test_query_params_serialization(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": []}})

    option = Option(wifi=True, lunch=True, midnight=False)
    client_dummy.search(option)

    request = httpx_mock.get_request()
    params = dict(request.url.params)

    # wifi=True should be serialized to '1'
    # lunch=True should be serialized to '1'
    # midnight=False should be serialized to '0' (now included because of value is not None)

    assert params.get("wifi") == "1"
    assert params.get("lunch") == "1"
    assert params.get("midnight") == "0"


def test_list_serialization(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": []}})

    option = Option(budget=["B001", "B002"], credit_card=["VISA", "Master"])
    client_dummy.search(option)

    request = httpx_mock.get_request()
    params = dict(request.url.params)

    assert params.get("budget") == "B001,B002"
    assert params.get("credit_card") == "VISA,Master"


def test_zero_values_serialization(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": []}})

    option = Option(lat=0.0, lng=0.0)
    client_dummy.search(option)

    request = httpx_mock.get_request()
    params = dict(request.url.params)

    assert params.get("lat") == "0.0"
    assert params.get("lng") == "0.0"


def test_order_未指定なら送らない(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": []}})

    client_dummy.search(Option(lat=35.0, lng=135.0))

    params = dict(httpx_mock.get_request().url.params)
    # 未指定なら API の既定 (位置検索は距離順) に任せる
    assert "order" not in params


def test_order_指定(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": []}})

    client_dummy.search(Option(lat=35.0, lng=135.0, order=4))

    params = dict(httpx_mock.get_request().url.params)
    assert params.get("order") == "4"


def test_複数指定パラメータのリスト変換(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": []}})

    option = Option(
        id=["J000000001", "J000000002"],
        special=["LT0086", "LT0045"],
        special_or=["LT0086", "LT0045"],
        special_category=["SPD1", "SPD3"],
        special_category_or=["SPD1", "SPD3"],
        service_area=["SA11", "SA12"],
        large_area=["Z011", "Z012"],
        middle_area=["Y005", "Y006"],
        small_area=["X010", "X011"],
        genre=["G001", "G002"],
    )
    client_dummy.search(option)

    params = dict(httpx_mock.get_request().url.params)
    assert params.get("id") == "J000000001,J000000002"
    assert params.get("special") == "LT0086,LT0045"
    assert params.get("special_or") == "LT0086,LT0045"
    assert params.get("special_category") == "SPD1,SPD3"
    assert params.get("special_category_or") == "SPD1,SPD3"
    assert params.get("service_area") == "SA11,SA12"
    assert params.get("large_area") == "Z011,Z012"
    assert params.get("middle_area") == "Y005,Y006"
    assert params.get("small_area") == "X010,X011"
    assert params.get("genre") == "G001,G002"


def test_複数指定パラメータの文字列はそのまま送る(client_dummy, httpx_mock):
    httpx_mock.add_response(json={"results": {"shop": []}})

    # 文字列は個数を検証しない (超えた分は API が無視する)
    client_dummy.search(Option(large_area="Z011,Z012,Z013,Z014"))

    params = dict(httpx_mock.get_request().url.params)
    assert params.get("large_area") == "Z011,Z012,Z013,Z014"


@pytest.mark.parametrize(
    ("field", "limit"),
    [
        ("id", 20),
        ("service_area", 3),
        ("large_area", 3),
        ("middle_area", 5),
        ("small_area", 5),
        ("budget", 2),
    ],
)
def test_複数指定パラメータの個数上限(field, limit):
    codes = [f"C{i:03}" for i in range(limit + 1)]

    Option.model_validate({field: codes[:limit]})
    with pytest.raises(ValidationError):
        Option.model_validate({field: codes})


@pytest.mark.parametrize(
    ("field", "valid", "invalid"),
    [
        ("count", [1, 100], [0, 101]),
        ("start", [1], [0]),
        ("order", [1, 4], [0, 5]),
    ],
)
def test_値域の検証(field, valid, invalid):
    for v in valid:
        Option.model_validate({field: v})
    for v in invalid:
        with pytest.raises(ValidationError):
            Option.model_validate({field: v})
