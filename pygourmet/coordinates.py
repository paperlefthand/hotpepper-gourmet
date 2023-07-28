from geopy.distance import geodesic


class Coordinates:
    """座標クラス"""

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def get_point(self) -> tuple[float, float]:
        """緯度と経度のペア"""
        return (self.latitude, self.longitude)

    def get_distance_m(self, coordinates) -> float:
        """2点間の測地距離[m]"""
        source = self.get_point()
        destination = coordinates.get_point()
        distance = geodesic(source, destination)
        return distance.m
