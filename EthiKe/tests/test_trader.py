def test_create_trader_success(client, auth_headers):
    response = client.post(
        "/traders/",
        json={"name": "Almaz", "phone_number": "0911000111"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Almaz"
    assert "trader_id" in body


def test_create_trader_missing_required_field_is_validation_error(client, auth_headers):
    response = client.post("/traders/", json={"name": "No phone"}, headers=auth_headers)
    assert response.status_code == 422


def test_list_traders_as_admin(client, admin_headers, trader):
    response = client.get("/traders/", headers=admin_headers)
    assert response.status_code == 200
    ids = [t["trader_id"] for t in response.json()]
    assert trader["trader_id"] in ids


def test_list_traders_as_trader_is_forbidden(client, auth_headers, trader):
    response = client.get("/traders/", headers=auth_headers)
    assert response.status_code == 403


def test_get_trader_success(client, auth_headers, trader):
    response = client.get(f"/traders/{trader['trader_id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["trader_id"] == trader["trader_id"]


def test_get_trader_not_found(client, admin_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/traders/{fake_id}", headers=admin_headers)
    assert response.status_code == 404


def test_get_trader_forbidden_for_unrelated_trader(
    client, other_trader_headers, trader
):
    """A trader with no ownership of this trader_id gets 403, not a 404 leak."""
    response = client.get(
        f"/traders/{trader['trader_id']}", headers=other_trader_headers
    )
    assert response.status_code == 403


def test_get_trader_malformed_uuid_is_validation_error(client, auth_headers):
    response = client.get("/traders/not-a-uuid", headers=auth_headers)
    assert response.status_code == 422


def test_patch_trader(client, auth_headers, trader):
    response = client.patch(
        f"/traders/{trader['trader_id']}",
        json={"city": "Bahir Dar"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["city"] == "Bahir Dar"


def test_put_trader_replaces_full_resource(client, auth_headers, trader):
    response = client.put(
        f"/traders/{trader['trader_id']}",
        json={"name": "Almaz Bekele", "phone_number": "0911000111", "city": "Hawassa"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Almaz Bekele"
    assert body["city"] == "Hawassa"


def test_delete_trader_as_trader_is_forbidden(client, auth_headers, trader):
    response = client.delete(f"/traders/{trader['trader_id']}", headers=auth_headers)
    assert response.status_code == 403


def test_delete_trader_as_admin_succeeds(client, admin_headers, trader):
    response = client.delete(f"/traders/{trader['trader_id']}", headers=admin_headers)
    assert response.status_code == 204


def test_delete_trader_not_found(client, admin_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/traders/{fake_id}", headers=admin_headers)
    assert response.status_code == 404


def test_get_trader_unauthenticated_is_401(client, trader):
    response = client.get(f"/traders/{trader['trader_id']}")
    assert response.status_code == 401
