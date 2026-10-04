def test_price_recommendation_returns_valid_shape(client, auth_headers, product):
    response = client.get(
        f"/predictions/price-recommendation/{product['product_id']}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_replacement_cost"] >= 0
    assert body["recommended_selling_price"] >= body["predicted_replacement_cost"]


def test_price_recommendation_uses_purchase_history(
    client, auth_headers, purchase, product
):
    response = client.get(
        f"/predictions/price-recommendation/{product['product_id']}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_replacement_cost"] > 0
    assert body["recommended_selling_price"] > body["predicted_replacement_cost"]


def test_risk_score_with_no_transactions_is_unknown_not_a_guess(
    client, auth_headers, trader
):
    """With zero recorded activity, the model has nothing to extrapolate from —
    this must return 'unknown' rather than running the model on all-zero
    input and returning a misleading score."""
    response = client.get(
        f"/predictions/risk-score/{trader['trader_id']}", headers=auth_headers
    )
    assert response.status_code == 200
    body = response.json()
    assert body["risk_label"] == "unknown"
    assert body["risk_score"] == 0.0


def test_price_recommendation_with_no_purchase_history_is_zero_not_a_guess(
    client, auth_headers, product
):
    response = client.get(
        f"/predictions/price-recommendation/{product['product_id']}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_replacement_cost"] == 0.0
    assert body["recommended_selling_price"] == 0.0


def test_risk_score_is_lower_when_income_covers_expenses(
    client, auth_headers, admin_headers, trader
):
    client.post(
        "/transactions/",
        json={
            "trader_id": trader["trader_id"],
            "type": "sale",
            "amount": "5000.00",
            "payment_method": "cash",
        },
        headers=auth_headers,
    )
    healthy_score = client.get(
        f"/predictions/risk-score/{trader['trader_id']}", headers=auth_headers
    ).json()["risk_score"]

    risky_trader = client.post(
        "/traders/",
        json={"name": "Risky Trader", "phone_number": "0922000222"},
        headers=admin_headers,
    ).json()
    client.post(
        "/transactions/",
        json={
            "trader_id": risky_trader["trader_id"],
            "type": "sale",
            "amount": "500.00",
            "payment_method": "cash",
        },
        headers=admin_headers,
    )
    client.post(
        "/transactions/",
        json={
            "trader_id": risky_trader["trader_id"],
            "type": "expense",
            "amount": "800.00",
            "payment_method": "cash",
        },
        headers=admin_headers,
    )
    client.post(
        "/transactions/",
        json={
            "trader_id": risky_trader["trader_id"],
            "type": "personal_withdrawal",
            "amount": "400.00",
            "payment_method": "cash",
        },
        headers=admin_headers,
    )
    client.post(
        "/credits/",
        json={
            "trader_id": risky_trader["trader_id"],
            "customer_name": "Debtor",
            "amount_owed": "1000.00",
        },
        headers=admin_headers,
    )
    risky_score = client.get(
        f"/predictions/risk-score/{risky_trader['trader_id']}", headers=admin_headers
    ).json()["risk_score"]

    assert healthy_score <= risky_score


def test_predictions_require_auth(client, product):
    response = client.get(f"/predictions/price-recommendation/{product['product_id']}")
    assert response.status_code == 401


def test_price_recommendation_forbidden_for_other_trader(
    client, other_trader_headers, product
):
    response = client.get(
        f"/predictions/price-recommendation/{product['product_id']}",
        headers=other_trader_headers,
    )
    assert response.status_code == 403


def test_risk_score_forbidden_for_other_trader(client, other_trader_headers, trader):
    response = client.get(
        f"/predictions/risk-score/{trader['trader_id']}", headers=other_trader_headers
    )
    assert response.status_code == 403
