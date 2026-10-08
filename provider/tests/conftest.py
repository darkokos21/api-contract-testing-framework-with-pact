import os

import pytest


@pytest.fixture
def broker_url():
    return os.getenv(
        "PACT_BROKER_BASE_URL",
        "http://localhost:9292",
    )


@pytest.fixture
def broker_username():
    return os.getenv(
        "PACT_BROKER_USERNAME",
        "pact",
    )


@pytest.fixture
def broker_password():
    return os.getenv(
        "PACT_BROKER_PASSWORD",
        "pact",
    )