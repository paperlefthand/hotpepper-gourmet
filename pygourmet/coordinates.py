# https://qiita.com/Yuzu2yan/items/0f312954feeb3c83c70e
import math

EARTH_RAD = 6378.137  # km


def deg_2_rad(deg: float) -> float:
    return deg * math.pi / 180.0


class Coordinates:
    """座標クラス"""

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def get_point(self) -> tuple[float, float]:
        """緯度と経度のペア"""
        return (self.latitude, self.longitude)

    def get_distance_km(self, coordinates) -> float:
        """2点間の測地距離[km]"""
        a_deg = self.get_point()
        b_deg = coordinates.get_point()
        a = (deg_2_rad(a_deg[0]), deg_2_rad(a_deg[1]))  # (lat, lon)
        b = (deg_2_rad(b_deg[0]), deg_2_rad(b_deg[1]))  # (lat, lon)

        distance = EARTH_RAD * math.acos(
            math.sin(a[0]) * math.sin(b[0])
            + math.cos(a[0]) * math.cos(b[0]) * math.cos(b[1] - a[1])
        )
        return distance
