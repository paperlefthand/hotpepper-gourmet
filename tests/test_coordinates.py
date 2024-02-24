from pygourmet import Coordinates


def test_get_distance_km():
    source = Coordinates(35.170915, 136.877417)
    destination = Coordinates(35.180915, 136.887417)
    distance = source.get_distance_km(destination)
    assert distance > 1.4 and distance < 1.5
    assert source.get_distance_km(source) < 1e-04
