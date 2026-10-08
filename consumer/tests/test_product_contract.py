from pact import match

from src.product_client import ProductClient


def test_get_product_contract(pact):
    """Verify the consumer's expectations for ProductService."""

    (
        pact.upon_receiving("a request for an existing product")
        .given("product 101 exists")
        .with_request(
            method="GET",
            path="/products/101",
        )
        .will_respond_with(200)
        .with_header(
            "Content-Type",
            match.regex(
                "application/json",
                regex=r"application/json.*",
            ),
        )
        .with_body(
            {
                "id": match.integer(101),
                "name": match.regex(
                    "Laptop",
                    regex=r"^Laptop$",
                ),
                "price": match.decimal(1299.99),
                "available": match.boolean(True),
            }
        )
    )

    with pact.serve() as mock_server:
        client = ProductClient(str(mock_server.url))

        product = client.get_product(101)

        assert product["id"] == 101
        assert product["name"] == "Laptop"
        assert product["price"] == 1299.99
        assert product["available"] is True
