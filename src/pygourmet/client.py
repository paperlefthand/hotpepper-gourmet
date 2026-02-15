"""APIクライアントモジュール。

このモジュールは、ホットペッパーグルメ検索APIと通信するためのメインクライアントクラスを提供します。
同期および非同期の両方の検索メソッドをサポートしています。
"""

import json
from typing import Any

import httpx

from pygourmet.errors import SearchError
from pygourmet.option import Option
from pygourmet.shop import Shop


class Api:
    """ホットペッパーグルメ検索APIクライアント。

    ホットペッパーグルメ検索APIへのリクエストを管理し、レスポンスを店舗データのリストとして返します。

    Examples:
        同期クライアントの使用例:
        ```python
        from pygourmet.client import Api
        from pygourmet.option import Option

        client = Api(keyid="YOUR_API_KEY")
        option = Option(keyword="居酒屋")
        shops = client.search(option)
        for shop in shops:
            print(shop.name)
        ```

        非同期クライアントの使用例:
        ```python
        import asyncio
        from pygourmet.client import Api
        from pygourmet.option import Option

        async def main():
            client = Api(keyid="YOUR_API_KEY")
            option = Option(keyword="寿司")
            shops = await client.search_async(option)
            for shop in shops:
                print(shop.name)

        asyncio.run(main())
        ```
    """

    def __init__(self, keyid: str) -> None:
        """Apiクライアントを初期化します。

        Args:
            keyid (str): ホットペッパーWebサービスから発行されたAPIキー。
        """

        self.__base_url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
        self.keyid = keyid

    def __create_query_params(self, option: Option) -> dict[str, str]:
        """Optionオブジェクトからクエリパラメータを作成します。

        Args:
            option (Option): 検索オプション。

        Returns:
            dict[str, str]: APIリクエストに使用するクエリパラメータの辞書。
        """
        params = {
            key: value
            for key, value in option.model_dump().items()
            if value is not None
        }
        params["key"] = self.keyid
        params["format"] = "json"
        return params

    def __create_shop_list(self, resp: dict[str, Any]) -> list[Shop]:
        """APIレスポンスからShopオブジェクトのリストを作成します。

        Args:
            resp (dict[str, Any]): APIからのJSONレスポンス。

        Returns:
            list[Shop]: 店舗データのリスト。

        Raises:
            SearchError: APIがエラーを返した場合、またはパースに失敗した場合。
        """
        try:
            if "error" in resp["results"].keys():
                errors = resp["results"]["error"]
                messages = []
                for err in errors:
                    code = err["code"]
                    if code == 1000:
                        messages.append(f"サーバ障害エラー: {err.get('message')}")
                    elif code == 2000:
                        messages.append(
                            f"APIキーまたはIPアドレスの認証エラー: {err.get('message')}"
                        )
                    elif code == 3000:
                        messages.append(f"パラメータ不正エラー: {err.get('message')}")
                raise SearchError(",".join(messages))
            else:
                return [Shop(**data) for data in resp["results"]["shop"]]
        except SearchError:
            raise
        except Exception as e:
            raise SearchError(str(e))

    def search(self, option: Option) -> list[Shop]:
        """レストランを同期的に検索します。

        Args:
            option (Option): 検索条件を指定するオプション。

        Returns:
            list[Shop]: 検索条件に合致した店舗データのリスト。

        Raises:
            SearchError: APIリクエストまたはレスポンスの処理中にエラーが発生した場合。
        """

        params = self.__create_query_params(option=option)
        resp = httpx.get(
            url=self.__base_url,
            params=params,
        )
        resp_dict = json.loads(resp.text)
        return self.__create_shop_list(resp=resp_dict)

    async def search_async(self, option: Option) -> list[Shop]:
        """レストランを非同期的に検索します。

        Args:
            option (Option): 検索条件を指定するオプション。

        Returns:
            list[Shop]: 検索条件に合致した店舗データのリスト。

        Raises:
            SearchError: APIリクエストまたはレスポンスの処理中にエラーが発生した場合。
        """

        params = self.__create_query_params(option=option)
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=self.__base_url,
                params=params,
            )
        resp_dict = json.loads(resp.text)
        return self.__create_shop_list(resp=resp_dict)
