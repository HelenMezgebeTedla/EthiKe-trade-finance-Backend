import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-not-for-production"

from database import Base, get_db
from main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    from app.core.rate_limit import limiter

    limiter.reset()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _register(client, username, email, password, role):
    response = client.post(
        "/auth/register",
        json={"username": username, "email": email, "password": password, "role": role},
    )
    assert response.status_code == 201, f"{role} registration failed: {response.text}"
    return response.json()


def _login(client, username, password):
    response = client.post(
        "/auth/login", data={"username": username, "password": password}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_credentials(client):
    _register(client, "admin_user", "admin@example.com", "AdminPass123!", "admin")
    return {"username": "admin_user", "password": "AdminPass123!"}


@pytest.fixture
def admin_headers(client, admin_credentials):
    return _login(client, admin_credentials["username"], admin_credentials["password"])


@pytest.fixture
def trader_credentials(client):
    _register(client, "trader_user", "trader@example.com", "TraderPass123!", "trader")
    return {"username": "trader_user", "password": "TraderPass123!"}


@pytest.fixture
def trader_headers(client, trader_credentials):
    return _login(
        client, trader_credentials["username"], trader_credentials["password"]
    )


@pytest.fixture
def other_trader_credentials(client):
    """A second, unrelated trader account — used to prove one trader can't
    read or write another trader's data."""
    _register(
        client, "other_trader", "other_trader@example.com", "OtherPass123!", "trader"
    )
    return {"username": "other_trader", "password": "OtherPass123!"}


@pytest.fixture
def other_trader_headers(client, other_trader_credentials):
    return _login(
        client,
        other_trader_credentials["username"],
        other_trader_credentials["password"],
    )


@pytest.fixture
def auth_headers(trader_headers):
    return trader_headers


@pytest.fixture
def trader(client, trader_headers):
    """Creates the Trader business profile and links it to trader_headers'
    account — every other fixture below acts as this trader."""
    response = client.post(
        "/traders/",
        json={
            "name": "Almaz",
            "phone_number": "0911000111",
            "business_type": "grocery",
            "region": "Addis Ababa",
            "city": "Addis Ababa",
        },
        headers=trader_headers,
    )
    assert response.status_code == 201, f"Trader creation failed: {response.text}"
    return response.json()


@pytest.fixture
def other_trader(client, other_trader_headers):
    response = client.post(
        "/traders/",
        json={"name": "Bereket", "phone_number": "0922000222"},
        headers=other_trader_headers,
    )
    assert response.status_code == 201, f"Other trader creation failed: {response.text}"
    return response.json()


@pytest.fixture
def product(client, auth_headers, trader):
    response = client.post(
        "/products/",
        json={
            "trader_id": trader["trader_id"],
            "product_name": "Cooking oil 1L",
            "category": "staples",
            "unit": "liter",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201, f"Product creation failed: {response.text}"
    return response.json()


@pytest.fixture
def purchase(client, auth_headers, product, trader):
    response = client.post(
        "/purchases/",
        json={
            "product_id": product["product_id"],
            "trader_id": trader["trader_id"],
            "quantity": "20",
            "unit_cost_at_purchase": "150.00",
            "supplier": "Wholesaler A",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201, f"Purchase creation failed: {response.text}"
    return response.json()


@pytest.fixture
def transaction(client, auth_headers, trader):
    response = client.post(
        "/transactions/",
        json={
            "trader_id": trader["trader_id"],
            "type": "sale",
            "amount": "200.00",
            "payment_method": "cash",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201, f"Transaction creation failed: {response.text}"
    return response.json()


@pytest.fixture
def sale(client, auth_headers, transaction, product):
    response = client.post(
        "/sales/",
        json={
            "transaction_id": transaction["transaction_id"],
            "product_id": product["product_id"],
            "quantity_sold": "1",
            "unit_sale_price": "200.00",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201, f"Sale creation failed: {response.text}"
    return response.json()


@pytest.fixture
def credit(client, auth_headers, trader):
    response = client.post(
        "/credits/",
        json={
            "trader_id": trader["trader_id"],
            "customer_name": "Bekele",
            "amount_owed": "50.00",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201, f"Credit creation failed: {response.text}"
    return response.json()


@pytest.fixture
def price_index_point(client, admin_headers):
    """Price index rows are shared reference data — only admins can write them."""
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
    assert response.status_code == 201, f"Price index creation failed: {response.text}"
    return response.json()
