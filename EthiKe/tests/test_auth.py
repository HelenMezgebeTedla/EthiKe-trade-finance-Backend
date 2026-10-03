def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"username": "newuser", "email": "newuser@example.com", "password": "Passw0rd!", "role": "trader"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "newuser"
    assert "hashed_password" not in body  # never leak the hash


def test_register_duplicate_username_fails(client, admin_credentials):
    response = client.post(
        "/auth/register",
        json={"username": admin_credentials["username"], "email": "other@example.com", "password": "Passw0rd!"},
    )
    assert response.status_code == 400


def test_register_duplicate_email_fails(client, admin_credentials):
    response = client.post(
        "/auth/register",
        json={"username": "someone_else", "email": "admin@example.com", "password": "Passw0rd!"},
    )
    assert response.status_code == 400


def test_register_missing_field_is_validation_error(client):
    response = client.post("/auth/register", json={"username": "x"})
    assert response.status_code == 422


def test_register_short_password_is_validation_error(client):
    response = client.post(
        "/auth/register",
        json={"username": "shortpw", "email": "shortpw@example.com", "password": "short"},
    )
    assert response.status_code == 422


def test_login_success_returns_jwt(client, admin_credentials):
    response = client.post(
        "/auth/login",
        data={"username": admin_credentials["username"], "password": admin_credentials["password"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 20


def test_login_wrong_password_fails(client, admin_credentials):
    response = client.post(
        "/auth/login",
        data={"username": admin_credentials["username"], "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_login_unknown_user_fails(client):
    response = client.post("/auth/login", data={"username": "ghost", "password": "whatever"})
    assert response.status_code == 401


def test_protected_endpoint_without_token_is_unauthorized(client):
    response = client.get("/traders/")
    assert response.status_code == 401


def test_protected_endpoint_with_bad_token_is_unauthorized(client):
    response = client.get("/traders/", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401


def test_get_my_profile(client, admin_headers, admin_credentials):
    response = client.get("/auth/me", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["username"] == admin_credentials["username"]


def test_password_is_hashed_not_stored_in_plaintext(client, admin_headers):
    """The register response and /users/ listing must never expose hashed_password."""
    response = client.get("/users/", headers=admin_headers)
    assert response.status_code == 200
    for user in response.json():
        assert "hashed_password" not in user
        assert "password" not in user
