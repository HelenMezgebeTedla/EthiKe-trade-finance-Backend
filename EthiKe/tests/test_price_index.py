def test_create_index_point_as_admin(client, admin_headers):
    response = client.post(
        "/price-index/",
        json={
            "country": "Ethiopia",
            "category": "staples",
            "month": "2026-08-01",
            "index_value": "142.5",
        },
        headers=admin_headers,
    )
    assert response.status_code == 201


def test_create_index_point_as_trader_is_forbidden(client, auth_headers):
    response = client.post(
        "/price-index/",
        json={
            "country": "Ethiopia",
            "category": "staples",
            "month": "2026-08-01",
            "index_value": "142.5",
        },
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_create_index_point_missing_field_is_validation_error(client, admin_headers):
    response = client.post(
        "/price-index/", json={"country": "Ethiopia"}, headers=admin_headers
    )
    assert response.status_code == 422


def test_read_category_series_as_trader(client, auth_headers, price_index_point):
    response = client.get("/price-index/category/staples", headers=auth_headers)
    assert response.status_code == 200
    categories = [p["category"] for p in response.json()]
    assert "staples" in categories


def test_list_price_indices_any_authenticated_user(
    client, auth_headers, price_index_point
):
    response = client.get("/price-index/", headers=auth_headers)
    assert response.status_code == 200


def test_put_price_index_as_admin(client, admin_headers, price_index_point):
    response = client.put(
        f"/price-index/{price_index_point['price_index_id']}",
        json={
            "country": "Ethiopia",
            "category": "staples",
            "month": "2026-09-01",
            "index_value": "150.0",
        },
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert float(response.json()["index_value"]) == 150.0


def test_patch_price_index_as_admin(client, admin_headers, price_index_point):
    response = client.patch(
        f"/price-index/{price_index_point['price_index_id']}",
        json={"index_value": "160.0"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert float(response.json()["index_value"]) == 160.0


def test_patch_price_index_as_trader_is_forbidden(
    client, auth_headers, price_index_point
):
    response = client.patch(
        f"/price-index/{price_index_point['price_index_id']}",
        json={"index_value": "999.0"},
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_delete_price_index_as_admin(client, admin_headers, price_index_point):
    response = client.delete(
        f"/price-index/{price_index_point['price_index_id']}", headers=admin_headers
    )
    assert response.status_code == 204


def test_delete_price_index_as_trader_is_forbidden(
    client, auth_headers, price_index_point
):
    response = client.delete(
        f"/price-index/{price_index_point['price_index_id']}", headers=auth_headers
    )
    assert response.status_code == 403
