from fastapi import FastAPI, HTTPException


app = FastAPI(
    title="ProductService",
    version="1.0.0",
)


PRODUCTS = {
    101: {
        "id": 101,
        "name": "Laptop",
        "price": 1299.99,
        "available": True,
    },
    102: {
        "id": 102,
        "name": "Monitor",
        "price": 399.99,
        "available": True,
    },
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = PRODUCTS.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@app.post("/_pact/provider-state")
def provider_state(body: dict):
    """
    Minimal provider-state endpoint used by Pact verification.

    The demo uses an in-memory dataset, so the requested state
    is already available.
    """

    state = body.get("state")

    if state == "product 101 exists":
        PRODUCTS[101] = PRODUCTS[101]

    return {
        "state": state,
        "status": "ready",
    }