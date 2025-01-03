import json
from typing import Any

import httpx

from pygourmet.errors import SearchError
from pygourmet.option import Option
from pygourmet.shop import Shop


class Api:
    """APIクライアントクラス"""

    # TODO keyidを指定しないとエラーになるようにする
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

    def __create_shop_list(self, resp: dict[str, Any]) -> list[Shop]:
        try:
            if "error" in resp["results"].keys():
                errors = resp["results"]["error"]
                messages = []
                for err in errors:
                    code = err["code"]
                    if code == 1000:
                        messages.append(f"サーバ障害エラー: {err.get("message")}")
                    elif code == 2000:
                        messages.append(
                            f"APIキーまたはIPアドレスの認証エラー: {err.get("message")}"
                        )
                    elif code == 3000:
                        messages.append(f"パラメータ不正エラー: {err.get("message")}")
                raise SearchError(",".join(messages))
            else:
                return [Shop(**data) for data in resp["results"]["shop"]]
        except Exception as e:
            raise SearchError(str(e))

    def search(self, option: Option) -> list[Shop]:
        """レストランを検索

        :param option: 検索オプション
        :type option: Option
        :return: 店舗データのリスト
        :rtype: list[Shop]
        :raises: SearchError: if failed
        """

        params = self.__create_query_params(option=option)
        resp = httpx.get(
            url=self.__base_url,
            params=params,
        )
        resp_dict = json.loads(resp.text)
        return self.__create_shop_list(resp=resp_dict)

    async def search_async(self, option: Option) -> list[Shop]:
        """[非同期]レストランを検索

        :param option: 検索オプション
        :type option: Option
        :return: 店舗データのリスト
        :rtype: list[Shop]
        :raises: SearchError: if failed
        """

        params = self.__create_query_params(option=option)
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=self.__base_url,
                params=params,
            )
        resp_dict = json.loads(resp.text)
        return self.__create_shop_list(resp=resp_dict)
