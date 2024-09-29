import json

import httpx

from .option import Option
from .shop import Shop


class Api:
    """APIクライアントクラス

    Args:
        keyid (str): APIキー
    """

    BASE_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

    def __init__(self, keyid: str) -> None:
        """
        Args:
            keyid: Key ID assigned to the user
        """
        self.keyid = keyid

    def __create_query_params(self, option: Option) -> dict:
        params = {
            key: value for key, value in option.model_dump().items() if bool(value)
        }
        params["key"] = self.keyid
        params["format"] = "json"
        return params

    def __create_shop_list(self, resp: httpx.Response) -> list[Shop]:
        resp_dict = json.loads(resp.text)
        return [Shop(**data) for data in resp_dict["results"]["shop"]]

    def search(self, option: Option) -> list[Shop]:
        """レストランを検索"""

        params = self.__create_query_params(option=option)
        resp = httpx.get(
            url=self.BASE_URL,
            params=params,
        )

        return self.__create_shop_list(resp=resp)

    async def async_search(self, option: Option) -> list[Shop]:
        """[非同期]レストランを検索"""

        params = self.__create_query_params(option=option)
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=self.BASE_URL,
                params=params,
            )

        return self.__create_shop_list(resp=resp)
