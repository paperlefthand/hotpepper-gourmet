import json

import httpx

from pygourmet.option import Option


class Api:
    """Api class

    API 呼び出しクラス

    Attributes:

    """

    BASE_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

    def __init__(self, keyid: str) -> None:
        """
        Args:
            keyid (str): Key ID assigned to the user
        """
        self.keyid = keyid

    def __radius_to_range(self, radius: int) -> int:
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

        return range

    def search(self, option: Option) -> list[dict]:
        """レストランを検索"""

        params: dict = {"key": self.keyid, "format": "json"}

        if option.keyword:
            params["keyword"] = option.keyword
        if option.lat and option.lng:
            params["lat"] = option.lat
            params["lng"] = option.lng
        if option.radius:
            params["range"] = self.__radius_to_range(option.radius)
        if option.count:
            params["count"] = option.count

        resp = httpx.get(
            url=self.BASE_URL,
            params=params,
        )

        resp_dict = json.loads(resp.text)

        return resp_dict["results"]["shop"]

    async def async_search(self, option: Option) -> list[dict]:
        """[非同期]レストランを検索"""

        params: dict = {"key": self.keyid, "format": "json"}

        if option.keyword:
            params["keyword"] = option.keyword
        if option.lat and option.lng:
            params["lat"] = option.lat
            params["lng"] = option.lng
        if option.radius:
            params["range"] = self.__radius_to_range(option.radius)
        if option.count:
            params["count"] = option.count

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=self.BASE_URL,
                params=params,
            )

        resp_dict = json.loads(resp.text)

        return resp_dict["results"]["shop"]
