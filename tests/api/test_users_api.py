def test_create_user(user_api, user_data):
    try:
        response = user_api.create_user(user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["responseCode"] == 201
        assert data["message"] == "User created!"
    finally:
        user_api.delete_user(user_data["email"], user_data["password"])


def test_get_user_details(user_api, created_user):
    response = user_api.get_user(created_user["email"])

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert data["user"]["email"] == created_user["email"]
    assert data["user"]["name"] == created_user["name"]


def test_update_user(user_api, created_user):
    updated_user = {
        **created_user,
        "name": "Updated API User",
        "company": "Updated Test Company",
    }

    response = user_api.update_user(updated_user)

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert data["message"] == "User updated!"

    get_response = user_api.get_user(updated_user["email"])
    get_data = get_response.json()
    assert get_data["user"]["name"] == updated_user["name"]
    assert get_data["user"]["company"] == updated_user["company"]


def test_delete_user(user_api, created_user):
    response = user_api.delete_user(
        created_user["email"],
        created_user["password"],
    )

    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert data["message"] == "Account deleted!"
