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
