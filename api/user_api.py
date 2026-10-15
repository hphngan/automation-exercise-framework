from api.api_client import APIClient


class UserAPI:
    """Convenience wrapper for the user-related API endpoints."""

    def __init__(self, client):
        self.client = client if isinstance(client, APIClient) else APIClient(client)

    def create_user(self, user_data):
        return self.client.post("/api/createAccount", data=user_data)

    def verify_login(self, email=None, password=None):
        data = {}
        if email is not None:
            data["email"] = email
        if password is not None:
            data["password"] = password

        return self.client.post("/api/verifyLogin", data=data)

    def get_user(self, email):
        return self.client.get("/api/getUserDetailByEmail", params={"email": email})

    def update_user(self, user_data):
        return self.client.put("/api/updateAccount", data=user_data)

    def delete_user(self, email, password):
        return self.client.delete(
            "/api/deleteAccount", data={"email": email, "password": password}
        )
