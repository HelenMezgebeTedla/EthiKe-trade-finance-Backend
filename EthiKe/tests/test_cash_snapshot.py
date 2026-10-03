def test_get_latest_snapshot_before_compute_is_not_found(client, auth_headers, trader):
    response = client.get(f"/cash-snapshots/trader/{trader['trader_id']}/latest", headers=auth_headers)
    assert response.status_code == 404


def test_compute_and_read_snapshot(client, auth_headers, trader, sale):
    response = client.post(f"/cash-snapshots/trader/{trader['trader_id']}/compute", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert float(body["cash_on_hand"]) == 200.0
    assert float(body["working_capital"]) == 200.0

    response = client.get(f"/cash-snapshots/trader/{trader['trader_id']}/latest", headers=auth_headers)
    assert response.status_code == 200
    assert float(response.json()["working_capital"]) == 200.0


def test_patch_snapshot_allows_manual_override(client, auth_headers, admin_headers, trader, sale):
    computed = client.post(f"/cash-snapshots/trader/{trader['trader_id']}/compute", headers=auth_headers).json()
    response = client.patch(
        f"/cash-snapshots/{computed['cash_snapshot_id']}", json={"true_profit_estimate": "180.00"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert float(response.json()["true_profit_estimate"]) == 180.0


def test_delete_snapshot_as_admin(client, auth_headers, admin_headers, trader, sale):
    computed = client.post(f"/cash-snapshots/trader/{trader['trader_id']}/compute", headers=auth_headers).json()
    response = client.delete(f"/cash-snapshots/{computed['cash_snapshot_id']}", headers=admin_headers)
    assert response.status_code == 204


def test_compute_snapshot_forbidden_for_other_trader(client, other_trader_headers, trader):
    response = client.post(f"/cash-snapshots/trader/{trader['trader_id']}/compute", headers=other_trader_headers)
    assert response.status_code == 403


def test_get_latest_snapshot_forbidden_for_other_trader(client, other_trader_headers, trader):
    response = client.get(f"/cash-snapshots/trader/{trader['trader_id']}/latest", headers=other_trader_headers)
    assert response.status_code == 403


def test_list_snapshots_admin_only(client, auth_headers, admin_headers, trader, sale):
    client.post(f"/cash-snapshots/trader/{trader['trader_id']}/compute", headers=auth_headers)
    forbidden = client.get("/cash-snapshots/", headers=auth_headers)
    assert forbidden.status_code == 403
    ok = client.get("/cash-snapshots/", headers=admin_headers)
    assert ok.status_code == 200
