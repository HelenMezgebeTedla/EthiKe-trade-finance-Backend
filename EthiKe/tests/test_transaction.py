def test_create_transaction_success(client, auth_headers, trader):
    response = client.post(
        "/transactions/",
        json={"trader_id": trader["trader_id"], "type": "expense", "amount": "30.00", "payment_method": "cash"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["type"] == "expense"


def test_create_transaction_invalid_type_is_validation_error(client, auth_headers, trader):
    response = client.post(
        "/transactions/",
        json={"trader_id": trader["trader_id"], "type": "not-a-real-type", "amount": "10.00"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_list_trader_transactions(client, auth_headers, transaction, trader):
    response = client.get(f"/transactions/trader/{trader['trader_id']}", headers=auth_headers)
    assert response.status_code == 200
    ids = [t["transaction_id"] for t in response.json()]
    assert transaction["transaction_id"] in ids


def test_list_trader_transactions_forbidden_for_other_trader(client, other_trader_headers, trader):
    response = client.get(f"/transactions/trader/{trader['trader_id']}", headers=other_trader_headers)
    assert response.status_code == 403


def test_get_transaction_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/transactions/{fake_id}", headers=auth_headers)
    assert response.status_code == 404


def test_get_transaction_forbidden_for_other_trader(client, other_trader_headers, transaction):
    response = client.get(f"/transactions/{transaction['transaction_id']}", headers=other_trader_headers)
    assert response.status_code == 403


def test_put_transaction(client, auth_headers, transaction, trader):
    response = client.put(
        f"/transactions/{transaction['transaction_id']}",
        json={"trader_id": trader["trader_id"], "type": "sale", "amount": "500.00", "payment_method": "telebirr"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert float(response.json()["amount"]) == 500.0


def test_patch_transaction(client, auth_headers, transaction):
    response = client.patch(
        f"/transactions/{transaction['transaction_id']}", json={"notes": "updated note"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["notes"] == "updated note"


def test_delete_transaction_as_owner_succeeds(client, auth_headers, transaction):
    response = client.delete(f"/transactions/{transaction['transaction_id']}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_transaction_forbidden_for_other_trader(client, other_trader_headers, transaction):
    response = client.delete(f"/transactions/{transaction['transaction_id']}", headers=other_trader_headers)
    assert response.status_code == 403


def test_delete_transaction_as_admin(client, admin_headers, transaction):
    response = client.delete(f"/transactions/{transaction['transaction_id']}", headers=admin_headers)
    assert response.status_code == 204
