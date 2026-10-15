from api.api_client import APIClient


class ProductAPI:
    """Convenience wrapper for the product-related API endpoints."""

    def __init__(self, client):
        self.client = client if isinstance(client, APIClient) else APIClient(client)

    def get_products(self):
        return self.client.get("/api/productsList")

    def get_brands(self):
        return self.client.get("/api/brandsList")

    def search_product(self, query=None):
        data = {}
        if query is not None:
            data["search_product"] = query

        return self.client.post("/api/searchProduct", data=data)
