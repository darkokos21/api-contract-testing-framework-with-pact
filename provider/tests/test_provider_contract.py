import os

from pact import Verifier


PROVIDER_NAME = "ProductService"
PROVIDER_URL = os.getenv(
    "PROVIDER_URL",
    "http://localhost:8000",
)


def test_provider_contract(
    broker_url,
    broker_username,
    broker_password,
):
    """Verify ProductService against consumer contracts."""

    verifier = (
        Verifier(PROVIDER_NAME)
        .add_transport(url=PROVIDER_URL)
        .broker_source(
            broker_url,
            username=broker_username,
            password=broker_password,
        )
        .state_handler(
            f"{PROVIDER_URL}/_pact/provider-state",
            body=True,
        )
    )

    if os.getenv("CI"):
        verifier.set_publish_options(
            version=os.getenv(
                "PROVIDER_VERSION",
                os.getenv("GITHUB_SHA", "local"),
            ),
            branch=os.getenv(
                "GITHUB_REF_NAME",
                "main",
            ),
        )

    verifier.verify()