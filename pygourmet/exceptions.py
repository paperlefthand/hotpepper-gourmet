"""pygourmet.exceptions module
"""


class PyGourmetError(Exception):
    """PyGourmetError class

    Base class for PyGourmet errors

    """

    @property
    def message(self):
        """return exception message

        Returns the first argument used to construct this exception.

        Returns:
            str: exception message

        """
        return self.args[0]
