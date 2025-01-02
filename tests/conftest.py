import pytest

from pygourmet import Api


@pytest.fixture
def client_dummy():
    return Api("dummy")
