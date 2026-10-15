def test_get_all_products(product_api):
    response = product_api.get_products()

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert data["products"]
    assert {"id", "name", "price", "brand", "category"}.issubset(
        data["products"][0]
    )


def test_get_all_brands(product_api):
    response = product_api.get_brands()

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert data["brands"]
    assert {"id", "brand"}.issubset(data["brands"][0])


def test_search_existing_product(product_api):
    response = product_api.search_product("top")

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert data["products"]
    assert all("top" in str(product).lower() for product in data["products"])


def test_search_nonexistent_product(product_api):
    response = product_api.search_product("product-that-does-not-exist-987654321")

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert data["products"] == []


def test_search_without_required_parameter(product_api):
    response = product_api.search_product()

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 400
    assert "search_product parameter is missing" in data["message"]


def test_products_endpoint_wrong_http_method(api_client):
    response = api_client.post("/api/productsList")

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 405
    assert data["message"] == "This request method is not supported."
