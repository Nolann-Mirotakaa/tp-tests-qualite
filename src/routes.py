from flask import Blueprint, jsonify, request

from src.pricing import DEFAULT_PROMO_CODES, PricingError, applyPromoCode, calculateOrderTotal

orders_bp = Blueprint("orders", __name__)
orders = []


def reset_orders():
    orders.clear()


def _order_data(payload):
    if not isinstance(payload, dict):
        raise PricingError("JSON object required")
    required = ("items", "distance", "weight", "hour", "dayOfWeek")
    missing = [key for key in required if key not in payload]
    if missing:
        raise PricingError(f"missing required fields: {', '.join(missing)}")
    return calculateOrderTotal(
        payload["items"],
        payload["distance"],
        payload["weight"],
        payload.get("promoCode"),
        payload["hour"],
        payload["dayOfWeek"],
    )


def _error_response(error):
    return jsonify({"error": str(error)}), error.status_code


@orders_bp.route("/orders/simulate", methods=["POST"])
def simulate_order():
    payload = request.get_json(silent=True)
    try:
        result = _order_data(payload)
    except PricingError as error:
        return _error_response(error)
    return jsonify(result), 200


@orders_bp.route("/orders", methods=["POST"])
def create_order():
    payload = request.get_json(silent=True)
    try:
        result = _order_data(payload)
    except PricingError as error:
        return _error_response(error)
    order = {"id": max((item["id"] for item in orders), default=0) + 1, **result}
    orders.append(order)
    return jsonify(order), 201


@orders_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = next((item for item in orders if item["id"] == order_id), None)
    if order is None:
        return jsonify({"error": "order not found"}), 404
    return jsonify(order), 200


@orders_bp.route("/promo/validate", methods=["POST"])
def validate_promo():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not payload.get("code") or "subtotal" not in payload:
        return jsonify({"error": "code and subtotal are required"}), 400
    try:
        result = applyPromoCode(
            payload["subtotal"], payload["code"], DEFAULT_PROMO_CODES
        )
    except PricingError as error:
        return _error_response(error)
    return jsonify({"valid": True, **result, "newPrice": result["total"]}), 200
