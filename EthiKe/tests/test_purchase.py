def test_create_purchase_restocks_product(client, auth_headers, product, trader):
    response = client.post(
        "/purchases/",
        json={
            "product_id": product["product_id"],
            "trader_id": trader["trader_id"],
            "quantity": "10",
            "unit_cost_at_purchase": "100.00",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    updated_product = client.get(
        f"/products/{product['product_id']}", headers=auth_headers
    ).json()
    assert float(updated_product["current_stock_quantity"]) == 10.0


def test_create_purchase_missing_field_is_validation_error(
    client, auth_headers, product, trader
):
    response = client.post(
        "/purchases/",
        json={"product_id": product["product_id"], "trader_id": trader["trader_id"]},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_get_purchase_history(client, auth_headers, purchase, product):
    response = client.get(
        f"/purchases/product/{product['product_id']}", headers=auth_headers
    )
    assert response.status_code == 200
    ids = [p["purchase_id"] for p in response.json()]
    assert purchase["purchase_id"] in ids


def test_get_purchase_by_id(client, auth_headers, purchase):
    response = client.get(f"/purchases/{purchase['purchase_id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["purchase_id"] == purchase["purchase_id"]


def test_get_purchase_forbidden_for_other_trader(
    client, other_trader_headers, purchase
):
    response = client.get(
        f"/purchases/{purchase['purchase_id']}", headers=other_trader_headers
    )
    assert response.status_code == 403


def test_patch_purchase_adjusts_stock_by_delta(client, auth_headers, purchase, product):
    # purchase fixture bought 20 units, product now has 20 in stock
    response = client.patch(
        f"/purchases/{purchase['purchase_id']}",
        json={"quantity": "25"},
        headers=auth_headers,
    )
    assert response.status_code == 200

    updated_product = client.get(
        f"/products/{product['product_id']}", headers=auth_headers
    ).json()
    assert float(updated_product["current_stock_quantity"]) == 25.0


def test_put_purchase(client, auth_headers, purchase):
    response = client.put(
        f"/purchases/{purchase['purchase_id']}",
        json={"supplier": "New Supplier"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["supplier"] == "New Supplier"


def test_delete_purchase_reverses_stock(client, auth_headers, purchase, product):
    response = client.delete(
        f"/purchases/{purchase['purchase_id']}", headers=auth_headers
    )
    assert response.status_code == 204

    updated_product = client.get(
        f"/products/{product['product_id']}", headers=auth_headers
    ).json()
    assert float(updated_product["current_stock_quantity"]) == 0.0


def test_delete_purchase_forbidden_for_other_trader(
    client, other_trader_headers, purchase
):
    response = client.delete(
        f"/purchases/{purchase['purchase_id']}", headers=other_trader_headers
    )
    assert response.status_code == 403


def test_delete_purchase_as_admin(client, admin_headers, purchase):
    response = client.delete(
        f"/purchases/{purchase['purchase_id']}", headers=admin_headers
    )
    assert response.status_code == 204
