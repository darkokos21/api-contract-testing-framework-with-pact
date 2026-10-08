from pathlib import Path

import pytest
from pact import Pact


PACT_DIR = Path(__file__).resolve().parents[2] / "pacts"


@pytest.fixture
def pact():
    """Create a Pact consumer/provider contract."""

    pact = Pact(
        "OrderService",
        "ProductService",
    ).with_specification("V4")

    yield pact

    PACT_DIR.mkdir(parents=True, exist_ok=True)
    pact.write_file(PACT_DIR)