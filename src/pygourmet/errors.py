"""エラー定義モジュール。

このモジュールは、ライブラリ内で発生する例外クラスを定義します。
"""


class SearchError(Exception):
    """検索実行時に発生する例外。

    APIからのエラーレスポンスや、通信エラー、パースエラーなど、
    検索処理に関連するあらゆるエラーを表します。

    Attributes:
        message (str): エラーメッセージ。
    """

    def __init__(self, message: str) -> None:
        """SearchErrorを初期化します。

        Args:
            message (str): エラーメッセージ。
        """
        self.message = message
        super().__init__(self.message)
