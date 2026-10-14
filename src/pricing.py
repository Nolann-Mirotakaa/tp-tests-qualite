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
