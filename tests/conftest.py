import pytest

from pygourmet import Api


@pytest.fixture
def client():
    return Api("dummy")
