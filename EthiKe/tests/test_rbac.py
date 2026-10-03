def test_trader_can_create_own_profile(client, trader_headers):
    response = client.post(
        "/traders/", json={"name": "Self-created", "phone_number": "0900000001"}, headers=trader_headers
    )
    assert response.status_code == 201


def test_trader_cannot_delete_own_trader_profile(client, trader_headers, trader):
    response = client.delete(f"/traders/{trader['trader_id']}", headers=trader_headers)
    assert response.status_code == 403


def test_admin_can_delete_trader(client, admin_headers, trader):
    response = client.delete(f"/traders/{trader['trader_id']}", headers=admin_headers)
    assert response.status_code == 204


def test_trader_cannot_list_all_traders(client, trader_headers):
    response = client.get("/traders/", headers=trader_headers)
    assert response.status_code == 403


def test_admin_can_list_all_traders(client, admin_headers, trader):
    response = client.get("/traders/", headers=admin_headers)
    assert response.status_code == 200


def test_trader_cannot_access_another_traders_profile(client, trader_headers, other_trader):
    response = client.get(f"/traders/{other_trader['trader_id']}", headers=trader_headers)
    assert response.status_code == 403


def test_trader_cannot_access_another_traders_products(client, other_trader_headers, product):
    """`product` belongs to `trader`; other_trader_headers must not see it."""
    response = client.get(f"/products/trader/{product['trader_id']}", headers=other_trader_headers)
    assert response.status_code == 403


def test_admin_can_access_any_traders_products(client, admin_headers, product):
    response = client.get(f"/products/trader/{product['trader_id']}", headers=admin_headers)
    assert response.status_code == 200


def test_trader_cannot_list_users(client, trader_headers):
    response = client.get("/users/", headers=trader_headers)
    assert response.status_code == 403


def test_admin_can_list_users(client, admin_headers):
    response = client.get("/users/", headers=admin_headers)
    assert response.status_code == 200


def test_trader_cannot_create_user(client, trader_headers):
    response = client.post(
        "/users/",
        json={"username": "sneaky", "email": "sneaky@example.com", "password": "Passw0rd!", "role": "admin"},
        headers=trader_headers,
    )
    assert response.status_code == 403


def test_admin_can_create_user(client, admin_headers):
    response = client.post(
        "/users/",
        json={"username": "new_trader", "email": "new_trader@example.com", "password": "Passw0rd!", "role": "trader"},
        headers=admin_headers,
    )
    assert response.status_code == 201


def test_trader_cannot_write_price_index(client, trader_headers):
    response = client.post(
        "/price-index/",
        json={"country": "Kenya", "category": "staples", "month": "2026-08-01", "index_value": "100.0"},
        headers=trader_headers,
    )
    assert response.status_code == 403


def test_any_authenticated_user_can_read_price_index(client, trader_headers, price_index_point):
    response = client.get("/price-index/", headers=trader_headers)
    assert response.status_code == 200


def test_trader_creating_resource_ignores_spoofed_trader_id(client, trader_headers, trader, other_trader):
    """A trader trying to create a product under someone else's trader_id gets
    silently redirected to their OWN trader_id instead — never a 403 here,
    because the server corrects it rather than trusting client input."""
    response = client.post(
        "/products/",
        json={"trader_id": other_trader["trader_id"], "product_name": "Sneaky product"},
        headers=trader_headers,
    )
    assert response.status_code == 201
    assert response.json()["trader_id"] == trader["trader_id"]
