import math


class PricingError(ValueError):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


def _finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise PricingError(f"{name} must be a finite number")
    return float(value)


def calculateDeliveryFee(distance, weight):
    distance = _finite_number(distance, "distance")
    weight = _finite_number(weight, "weight")
    if distance < 0 or weight < 0:
        raise PricingError("distance and weight must be non-negative")
    if distance > 10:
        return None
    fee = 2 + max(0, distance - 3) * 0.5
    if weight > 5:
        fee += 1.5
    return round(fee, 2)



def applyPromoCode(subtotal, promoCode, promoCodes, today=None):
    from datetime import date

    subtotal = _finite_number(subtotal, "subtotal")
    if subtotal < 0:
        raise PricingError("subtotal must be non-negative")
    subtotal = round(subtotal, 2)
    if not promoCode:
        return {"subtotal": subtotal, "discount": 0.0, "total": subtotal}
    promo = next(
        (item for item in (promoCodes or []) if item.get("code", "").casefold() == str(promoCode).casefold()),
        None,
    )
    if promo is None:
        raise PricingError("promo code not found", 404)
    today = today or date.today()
    try:
        expires_at = date.fromisoformat(promo["expiresAt"])
    except (KeyError, TypeError, ValueError) as error:
        raise PricingError("promo code has an invalid expiration date") from error
    if expires_at < today:
        raise PricingError("promo code has expired")
    minimum = _finite_number(promo.get("minOrder", 0), "minOrder")
    if subtotal < minimum:
        raise PricingError("subtotal is below the promo minimum order")
    value = _finite_number(promo.get("value"), "promo value")
    if value < 0:
        raise PricingError("promo value must be non-negative")
    if promo.get("type") == "percentage":
        discounted = subtotal * (1 - value / 100)
    elif promo.get("type") == "fixed":
        discounted = subtotal - value
    else:
        raise PricingError("promo type must be percentage or fixed")
    total = round(max(0, discounted), 2)
    return {"subtotal": subtotal, "discount": round(subtotal - total, 2), "total": total}
