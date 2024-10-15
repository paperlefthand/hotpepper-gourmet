import json

import httpx

from .option import Option
from .shop import Shop


class Api:
    """APIクライアントクラス"""

    def __init__(self, keyid: str) -> None:
        """_summary_

        :param keyid: Key ID assigned to the user
        :type keyid: str
        """

        self.__base_url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
        self.keyid = keyid

    def __create_query_params(self, option: Option) -> dict[str, str]:
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
        """レストランを検索

        :param option: 検索オプション
        :type option: Option
        :return: 店舗データのリスト
        :rtype: list[Shop]
        """

        params = self.__create_query_params(option=option)
        resp = httpx.get(
            url=self.__base_url,
            params=params,
        )

        return self.__create_shop_list(resp=resp)

    async def async_search(self, option: Option) -> list[Shop]:
        """[非同期]レストランを検索"""

        params = self.__create_query_params(option=option)
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=self.__base_url,
                params=params,
            )

        return self.__create_shop_list(resp=resp)
