"""
    API Impl
"""
import logging
import json
# from typing import List, Optional, Tuple, Union

import requests

# from requests.models import Response

from pygourmet.error import PyGourmetError

logger = logging.getLogger(__name__)


class Api:
    """Api

    API 呼び出しクラス

    """
    BASE_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

    def __init__(self, keyid: str) -> None:
        """
        Init the Api instance

        :param keyid: Key ID assigned to the user
        """
        if bool(keyid):
            self.keyid = keyid
        else:
            raise PyGourmetError("Invalid keyid")

    def get_restaurants(
        self,
        lat: float,
        lng: float,
        radius: int = 1000,
        count: int = 10,
    ) -> dict:
        """
        Search restaurants by location

        :param lat: latitude of POI
        :param lng: longitude of POI
        :param radius: search range from POI
        :param count: max result counts
        """

        range = 3
        if radius <= 300:
            range = 1
        elif radius <= 500:
            range = 2
        elif radius <= 1000:
            range = 3
        elif radius <= 2000:
            range = 4
        elif radius > 2000:
            range = 5

        if (count < 0):
            raise PyGourmetError("Invalid count value (must be >= 0)")

        params = {
            "key": self.keyid,
            "lat": lat,
            "lng": lng,
            "range": range,
            "count": count,
            "format": "json",
        }

        resp = requests.get(
            url=self.BASE_URL,
            params=params,
        )

        resp_dict = json.loads(resp.text)

        return resp_dict["results"]["shop"]
