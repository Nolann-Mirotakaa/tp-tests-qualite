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



def calculateSurge(hour, dayOfWeek):
    hour = _finite_number(hour, "hour")
    if not 0 <= hour <= 24:
        raise PricingError("hour must be between 0 and 24")
    day = dayOfWeek.casefold() if isinstance(dayOfWeek, str) else ""
    days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
    if day not in days:
        raise PricingError("dayOfWeek must be a weekday name")
    if hour < 10 or hour >= 22:
        return 0
    if day == "sunday":
        return 1.2
    if day in {"friday", "saturday"} and 19 <= hour < 22:
        return 1.8
    if day in {"monday", "tuesday", "wednesday", "thursday"}:
        if 12 <= hour < 13.5:
            return 1.3
        if 19 <= hour < 22:
            return 1.5
    return 1.0
