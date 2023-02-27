import json
import os

import pytest

from pygourmet import Api


class Helpers:
    @staticmethod
    def load_json_data(filename):
        with open(filename, "rb") as f:
            return json.loads(f.read().decode("utf-8"))


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture
def api():
    return Api(keyid=os.environ.get("KEYID"))
