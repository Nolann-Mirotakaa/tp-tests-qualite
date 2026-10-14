import pytest

from src.app import app
from src.routes import orders, reset_orders


@pytest.fixture(autouse=True)
def clean_orders():
    reset_orders()


@pytest.fixture
def client():
    return app.test_client()


def valid_order(**overrides):
    payload = {
        "items": [{"name": "Pizza", "price": 12.5, "quantity": 2}],
        "distance": 5,
        "weight": 2,
        "hour": 15,
        "dayOfWeek": "tuesday",
    }
    payload.update(overrides)
    return payload


# POST /orders/simulate (7 integration tests)
def test_simulate_returns_price_for_normal_order(client):
    response = client.post("/orders/simulate", json=valid_order())
    assert response.status_code == 200
    assert response.get_json()["total"] == 28
    assert orders == []


def test_simulate_applies_valid_promo(client):
    response = client.post(
        "/orders/simulate", json=valid_order(promoCode="BIENVENUE20")
    )
    assert response.status_code == 200
    assert response.get_json()["discount"] == 5


def test_simulate_rejects_expired_promo(client):
    response = client.post("/orders/simulate", json=valid_order(promoCode="EXPIRE"))
    assert response.status_code == 400
    assert "expired" in response.get_json()["error"]


def test_simulate_rejects_empty_cart(client):
    assert client.post("/orders/simulate", json=valid_order(items=[])).status_code == 400


def test_simulate_rejects_out_of_zone_order(client):
    assert client.post("/orders/simulate", json=valid_order(distance=15)).status_code == 400


def test_simulate_rejects_closed_hours(client):
    assert client.post("/orders/simulate", json=valid_order(hour=23)).status_code == 400


def test_simulate_applies_friday_surge_to_delivery(client):
    response = client.post("/orders/simulate", json=valid_order(hour=20, dayOfWeek="friday"))
    assert response.status_code == 200
    assert response.get_json()["deliveryFee"] == 5.4


# POST /orders (5 integration tests)
def test_create_order_returns_201_with_generated_id(client):
    response = client.post("/orders", json=valid_order())
    assert response.status_code == 201
    assert response.get_json()["id"] == 1


def test_created_order_can_be_retrieved(client):
    created = client.post("/orders", json=valid_order()).get_json()
    response = client.get(f"/orders/{created['id']}")
    assert response.status_code == 200
    assert response.get_json() == created


def test_two_orders_receive_different_ids(client):
    first = client.post("/orders", json=valid_order()).get_json()
    second = client.post("/orders", json=valid_order()).get_json()
    assert first["id"] != second["id"]


def test_invalid_order_returns_400(client):
    assert client.post("/orders", json=valid_order(items=[])).status_code == 400


def test_invalid_order_is_not_saved(client):
    client.post("/orders", json=valid_order(distance=15))
    assert orders == []


# GET /orders/:id (3 integration tests)
def test_get_existing_order_returns_200(client):
    created = client.post("/orders", json=valid_order()).get_json()
    assert client.get(f"/orders/{created['id']}").status_code == 200


def test_get_unknown_order_returns_404(client):
    assert client.get("/orders/999").status_code == 404


def test_get_order_has_complete_response_structure(client):
    created = client.post("/orders", json=valid_order()).get_json()
    response = client.get(f"/orders/{created['id']}")
    assert set(response.get_json()) == {
        "id", "subtotal", "discount", "deliveryFee", "surge", "total"
    }


# POST /promo/validate (5 integration tests)
def test_validate_valid_promo_returns_discount_details(client):
    response = client.post("/promo/validate", json={"code": "BIENVENUE20", "subtotal": 25})
    assert response.status_code == 200
    assert response.get_json()["newPrice"] == 20


def test_validate_expired_promo_returns_400(client):
    response = client.post("/promo/validate", json={"code": "EXPIRE", "subtotal": 25})
    assert response.status_code == 400
    assert "expired" in response.get_json()["error"]


def test_validate_promo_below_minimum_returns_400(client):
    response = client.post("/promo/validate", json={"code": "BIENVENUE20", "subtotal": 10})
    assert response.status_code == 400
    assert "minimum" in response.get_json()["error"]


def test_validate_unknown_promo_returns_404(client):
    assert client.post(
        "/promo/validate", json={"code": "UNKNOWN", "subtotal": 25}
    ).status_code == 404


def test_validate_promo_without_code_returns_400(client):
    assert client.post("/promo/validate", json={"subtotal": 25}).status_code == 400
