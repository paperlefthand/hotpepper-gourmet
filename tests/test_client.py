def test_radius_to_range(api):
    assert api._Api__radius_to_range(500) == 2
    assert api._Api__radius_to_range(1000) == 3
    assert api._Api__radius_to_range(1500) == 4
