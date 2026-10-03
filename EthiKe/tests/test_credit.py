def test_create_credit_success(client, auth_headers, trader):
    response = client.post(
        "/credits/",
        json={"trader_id": trader["trader_id"], "customer_name": "Bekele", "amount_owed": "50.00"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "open"


def test_list_open_credit(client, auth_headers, credit, trader):
    response = client.get(f"/credits/trader/{trader['trader_id']}/open", headers=auth_headers)
    assert response.status_code == 200
    ids = [c["credit_id"] for c in response.json()]
    assert credit["credit_id"] in ids


def test_list_open_credit_forbidden_for_other_trader(client, other_trader_headers, trader):
    response = client.get(f"/credits/trader/{trader['trader_id']}/open", headers=other_trader_headers)
    assert response.status_code == 403


def test_repay_credit_full_closes_it(client, auth_headers, credit):
    response = client.post(f"/credits/{credit['credit_id']}/repay", json={"amount": "50.00"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "closed"


def test_repay_credit_partial(client, auth_headers, credit):
    response = client.post(f"/credits/{credit['credit_id']}/repay", json={"amount": "20.00"}, headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "partial"
    assert float(body["amount_repaid"]) == 20.0


def test_repay_credit_forbidden_for_other_trader(client, other_trader_headers, credit):
    response = client.post(
        f"/credits/{credit['credit_id']}/repay", json={"amount": "10.00"}, headers=other_trader_headers
    )
    assert response.status_code == 403


def test_repay_credit_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(f"/credits/{fake_id}/repay", json={"amount": "10.00"}, headers=auth_headers)
    assert response.status_code == 404


def test_put_credit(client, auth_headers, credit, trader):
    response = client.put(
        f"/credits/{credit['credit_id']}",
        json={"trader_id": trader["trader_id"], "customer_name": "Updated Name", "amount_owed": "75.00"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Updated Name"


def test_patch_credit(client, auth_headers, credit):
    response = client.patch(f"/credits/{credit['credit_id']}", json={"customer_name": "Renamed"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Renamed"


def test_delete_credit_as_owner(client, auth_headers, credit):
    response = client.delete(f"/credits/{credit['credit_id']}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_credit_as_admin(client, admin_headers, credit):
    response = client.delete(f"/credits/{credit['credit_id']}", headers=admin_headers)
    assert response.status_code == 204
