def test_create_sale_reduces_stock(
    client, auth_headers, purchase, transaction, product
):
    stocked_product = client.get(
        f"/products/{product['product_id']}", headers=auth_headers
    ).json()
    starting_stock = float(stocked_product["current_stock_quantity"])

    response = client.post(
        "/sales/",
        json={
            "transaction_id": transaction["transaction_id"],
            "product_id": product["product_id"],
            "quantity_sold": "2",
            "unit_sale_price": "200.00",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    updated_product = client.get(
        f"/products/{product['product_id']}", headers=auth_headers
    ).json()
    assert float(updated_product["current_stock_quantity"]) == starting_stock - 2


def test_create_sale_missing_field_is_validation_error(
    client, auth_headers, transaction, product
):
    response = client.post(
        "/sales/",
        json={
            "transaction_id": transaction["transaction_id"],
            "product_id": product["product_id"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_create_sale_forbidden_for_other_trader(
    client, other_trader_headers, transaction, product
):
    """other_trader can't create a sale against a transaction that isn't theirs."""
    response = client.post(
        "/sales/",
        json={
            "transaction_id": transaction["transaction_id"],
            "product_id": product["product_id"],
            "quantity_sold": "1",
            "unit_sale_price": "50.00",
        },
        headers=other_trader_headers,
    )
    assert response.status_code == 403


def test_list_product_sales(client, auth_headers, sale, product):
    response = client.get(
        f"/sales/product/{product['product_id']}", headers=auth_headers
    )
    assert response.status_code == 200
    ids = [s["sale_id"] for s in response.json()]
    assert sale["sale_id"] in ids


def test_get_sale_forbidden_for_other_trader(client, other_trader_headers, sale):
    response = client.get(f"/sales/{sale['sale_id']}", headers=other_trader_headers)
    assert response.status_code == 403


def test_patch_sale_adjusts_stock_by_delta(client, auth_headers, sale, product):
    # sale fixture sold 1 unit already
    response = client.patch(
        f"/sales/{sale['sale_id']}", json={"quantity_sold": "3"}, headers=auth_headers
    )
    assert response.status_code == 200

    updated_product = client.get(
        f"/products/{product['product_id']}", headers=auth_headers
    ).json()
    # started at 0, purchase fixture not used here, so -3 total after patch (was -1)
    assert float(updated_product["current_stock_quantity"]) == -3.0


def test_delete_sale_restores_stock(client, auth_headers, sale, product):
    response = client.delete(f"/sales/{sale['sale_id']}", headers=auth_headers)
    assert response.status_code == 204

    updated_product = client.get(
        f"/products/{product['product_id']}", headers=auth_headers
    ).json()
    assert float(updated_product["current_stock_quantity"]) == 0.0


def test_delete_sale_as_admin(client, admin_headers, sale):
    response = client.delete(f"/sales/{sale['sale_id']}", headers=admin_headers)
    assert response.status_code == 204
