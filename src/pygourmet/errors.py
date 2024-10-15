class PyGourmetError(Exception):
    """Base class for PyGourmet errors"""

    @property
    def message(self) -> str:
        """エラーメッセージ

        :return: error message
        :rtype: str
        """

        return self.args[0]
