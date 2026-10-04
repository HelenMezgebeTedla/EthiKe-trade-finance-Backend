def test_create_product_success(client, auth_headers, trader):
    response = client.post(
        "/products/",
        json={"trader_id": trader["trader_id"], "product_name": "Sugar 1kg"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["product_name"] == "Sugar 1kg"
    assert float(body["current_stock_quantity"]) == 0


def test_create_product_missing_trader_is_validation_error(client, auth_headers):
    response = client.post(
        "/products/", json={"product_name": "No trader"}, headers=auth_headers
    )
    assert response.status_code == 422


def test_list_trader_products(client, auth_headers, product, trader):
    response = client.get(
        f"/products/trader/{trader['trader_id']}", headers=auth_headers
    )
    assert response.status_code == 200
    ids = [p["product_id"] for p in response.json()]
    assert product["product_id"] in ids


def test_list_trader_products_forbidden_for_other_trader(
    client, other_trader_headers, trader
):
    response = client.get(
        f"/products/trader/{trader['trader_id']}", headers=other_trader_headers
    )
    assert response.status_code == 403


def test_get_product_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/products/{fake_id}", headers=auth_headers)
    assert response.status_code == 404


def test_get_product_forbidden_for_other_trader(client, other_trader_headers, product):
    response = client.get(
        f"/products/{product['product_id']}", headers=other_trader_headers
    )
    assert response.status_code == 403


def test_get_product_ok_for_admin(client, admin_headers, product):
    response = client.get(f"/products/{product['product_id']}", headers=admin_headers)
    assert response.status_code == 200


def test_put_product(client, auth_headers, product, trader):
    response = client.put(
        f"/products/{product['product_id']}",
        json={
            "trader_id": trader["trader_id"],
            "product_name": "Sugar 2kg",
            "current_stock_quantity": "5",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["product_name"] == "Sugar 2kg"


def test_patch_product(client, auth_headers, product):
    response = client.patch(
        f"/products/{product['product_id']}",
        json={"category": "updated-category"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["category"] == "updated-category"


def test_patch_product_forbidden_for_other_trader(
    client, other_trader_headers, product
):
    response = client.patch(
        f"/products/{product['product_id']}",
        json={"category": "hijacked"},
        headers=other_trader_headers,
    )
    assert response.status_code == 403


def test_delete_product_as_owner_succeeds(client, auth_headers, product):
    response = client.delete(f"/products/{product['product_id']}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_product_forbidden_for_other_trader(
    client, other_trader_headers, product
):
    response = client.delete(
        f"/products/{product['product_id']}", headers=other_trader_headers
    )
    assert response.status_code == 403


def test_delete_product_as_admin_succeeds(client, admin_headers, product):
    response = client.delete(
        f"/products/{product['product_id']}", headers=admin_headers
    )
    assert response.status_code == 204


def test_unauthenticated_request_is_401(client, product):
    response = client.get(f"/products/{product['product_id']}")
    assert response.status_code == 401
