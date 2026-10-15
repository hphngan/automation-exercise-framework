def test_valid_login(user_api, created_user):
    response = user_api.verify_login(
        created_user["email"],
        created_user["password"],
    )

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert data["message"] == "User exists!"


def test_invalid_login(user_api):
    response = user_api.verify_login(
        "missing-user@example.com",
        "incorrect-password",
    )

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 404
    assert data["message"] == "User not found!"


def test_login_without_email(user_api):
    response = user_api.verify_login(password="password-only")

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 400
    assert "email or password parameter is missing" in data["message"]


def test_login_endpoint_wrong_http_method(api_client):
    response = api_client.delete("/api/verifyLogin")

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 405
    assert data["message"] == "This request method is not supported."
