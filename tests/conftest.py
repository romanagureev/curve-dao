import os

import boa
import pytest

import curve_dao


def pytest_sessionstart():
    boa.env.fork(url=os.getenv("RPC_ETHEREUM"), block_identifier=20679351)


@pytest.fixture(scope="session")
def etherscan_api_key():
    return os.getenv("ETHERSCAN_API_KEY")


@pytest.fixture(scope="session")
def pinata_token():
    return os.getenv("PINATA_TOKEN")


@pytest.fixture(scope="module")
def vote_creator():
    return curve_dao.addresses.CONVEX_VOTERPROXY
