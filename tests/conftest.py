import os

import pytest

from pygourmet import Api


@pytest.fixture
def client_dummy():
    return Api("dummy")


@pytest.fixture
def client():
    return Api(os.environ.get("HOTPEPPER_KEYID"))
