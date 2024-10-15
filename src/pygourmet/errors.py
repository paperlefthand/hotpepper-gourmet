class SearchError(Exception):
    """raise when search errors"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
