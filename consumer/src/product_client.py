import requests


class ProductClient:
    """HTTP client used by the consumer service."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_product(self, product_id: int) -> dict:
        response = requests.get(
            f"{self.base_url}/products/{product_id}",
            timeout=5,
        )
        response.raise_for_status()
        return response.json()