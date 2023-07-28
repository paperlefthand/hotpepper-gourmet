from pygourmet import Coordinates


def test_get_distance_m():
    source = Coordinates(35.170915, 136.877417)
    destination = Coordinates(35.180915, 136.887417)
    distance = source.get_distance_m(destination)
    assert distance > 1400 and distance < 1500

    assert source.get_distance_m(source) == 0
