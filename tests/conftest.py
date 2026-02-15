import pytest

from pygourmet import Api


def pytest_addoption(parser):
    # --run-integration というオプションを追加
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests with real API",
    )


def pytest_collection_modifyitems(config, items):
    # --run-integration が指定されていない場合、integration マーカーが付いたテストをスキップ
    if config.getoption("--run-integration"):
        return

    skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


@pytest.fixture
def client_dummy():
    return Api("dummy")
