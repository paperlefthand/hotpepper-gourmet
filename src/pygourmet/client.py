"""APIクライアントモジュール。

このモジュールは、ホットペッパーグルメ検索APIと通信するためのメインクライアントクラスを提供します。
同期および非同期の両方の検索メソッドをサポートしています。
"""

from typing import TypedDict, cast

import httpx
from pydantic import ValidationError

from pygourmet.errors import SearchError
from pygourmet.option import Option
from pygourmet.shop import Shop


class _ErrorItem(TypedDict):
    code: int
    message: str


class _Results(TypedDict, total=False):
    error: list[_ErrorItem]
    shop: list[dict[str, object]]


class _SearchResponse(TypedDict):
    results: _Results


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

        self.__base_url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
        self.keyid = keyid

    def __create_query_params(self, option: Option) -> dict[str, str | int | float]:
        """Optionオブジェクトからクエリパラメータを作成します。

        Args:
            option (Option): 検索オプション。

        Returns:
            dict[str, str | int | float]: APIリクエストに使用するクエリパラメータの辞書。
        """
        params: dict[str, str | int | float] = {
            key: value
            for key, value in option.model_dump().items()
            if value is not None
        }
        params["key"] = self.keyid
        params["format"] = "json"
        return params

    def __create_shop_list(self, resp: _SearchResponse) -> list[Shop]:
        """APIレスポンスからShopオブジェクトのリストを作成します。

        Args:
            resp (_SearchResponse): APIからのJSONレスポンス。

        Returns:
            list[Shop]: 店舗データのリスト。

        Raises:
            SearchError: APIがエラーを返した場合、またはパースに失敗した場合。
        """
        # NOTE 想定外のレスポンス構造 (KeyError, TypeError) と
        # Shop モデルへの変換失敗 (ValidationError) のみを SearchError に変換する
        try:
            results = resp["results"]
            if "error" in results:
                errors = results["error"]
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
                    else:
                        messages.append(f"エラー (code={code}): {err.get('message')}")
                raise SearchError(",".join(messages))
            return [Shop.model_validate(data) for data in results.get("shop", [])]
        except (KeyError, TypeError, ValidationError) as e:
            raise SearchError(str(e)) from e

    def __mask_key(self, message: str) -> str:
        """メッセージに含まれるAPIキーを伏せ字にします。

        Args:
            message (str): 元のメッセージ。

        Returns:
            str: APIキーを `***` に置き換えたメッセージ。
        """
        return message.replace(self.keyid, "***") if self.keyid else message

    def __request_error(self, e: httpx.RequestError) -> SearchError:
        """通信エラーをSearchErrorに変換します。

        Args:
            e (httpx.RequestError): httpx が送出した通信エラー。

        Returns:
            SearchError: 利用者に見せる例外。
        """
        return SearchError(self.__mask_key(f"通信エラー: {type(e).__name__}: {e}"))

    def __parse_response(self, resp: httpx.Response) -> list[Shop]:
        """HTTPレスポンスを検証し、Shopオブジェクトのリストを作成します。

        Args:
            resp (httpx.Response): APIからのHTTPレスポンス。

        Returns:
            list[Shop]: 店舗データのリスト。

        Raises:
            SearchError: ステータスコードが200以外の場合、本文がJSONでない場合、
                APIがエラーを返した場合、またはパースに失敗した場合。
        """
        # NOTE API はエラーでも 200 を返すため, 200 以外はプロキシやメンテナンスによるもの.
        # httpx の raise_for_status() はメッセージに URL (API キーを含む) を入れるため使わない
        if resp.status_code != httpx.codes.OK:
            raise SearchError(f"HTTPエラー: ステータスコード {resp.status_code}")
        try:
            resp_dict = cast(_SearchResponse, resp.json())
        except ValueError as e:
            raise SearchError(f"レスポンスがJSONではありません: {e}") from e
        return self.__create_shop_list(resp=resp_dict)

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
        try:
            resp = httpx.get(
                url=self.__base_url,
                params=params,
            )
        except httpx.RequestError as e:
            raise self.__request_error(e) from e
        return self.__parse_response(resp=resp)

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
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    url=self.__base_url,
                    params=params,
                )
        except httpx.RequestError as e:
            raise self.__request_error(e) from e
        return self.__parse_response(resp=resp)
