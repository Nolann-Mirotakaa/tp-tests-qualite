from datetime import date

import pytest

from src.pricing import (
    PricingError,
    applyPromoCode,
    calculateDeliveryFee,
    calculateOrderTotal,
    calculateSurge,
)


def test_delivery_fee_seven_kilometers():
    assert calculateDeliveryFee(7, 3) == 4.0


def test_delivery_fee_adds_heavy_package_surcharge():
    assert calculateDeliveryFee(5, 8) == 4.5


def test_delivery_fee_exactly_three_kilometers_has_only_base_fee():
    assert calculateDeliveryFee(3, 2) == 2.0


def test_delivery_fee_accepts_ten_kilometers_and_heavy_package():
    assert calculateDeliveryFee(10, 6) == 7.0


def test_delivery_fee_rejects_distance_over_ten_kilometers():
    assert calculateDeliveryFee(15, 1) is None


def test_delivery_fee_rejects_negative_distance():
    with pytest.raises(PricingError):
        calculateDeliveryFee(-1, 1)


def test_delivery_fee_rejects_negative_weight():
    with pytest.raises(PricingError):
        calculateDeliveryFee(1, -1)


def test_delivery_fee_allows_zero_distance():
    assert calculateDeliveryFee(0, 1) == 2.0


PROMOS = [
    {"code": "PERCENT20", "type": "percentage", "value": 20, "minOrder": 15, "expiresAt": "2099-12-31"},
    {"code": "FIXED5", "type": "fixed", "value": 5, "minOrder": 0, "expiresAt": "2099-12-31"},
    {"code": "EXPIRED", "type": "fixed", "value": 2, "minOrder": 0, "expiresAt": "2020-01-01"},
]


def test_promo_applies_percentage_discount():
    result = applyPromoCode(50, "PERCENT20", PROMOS, today=date(2025, 1, 1))
    assert result == {"subtotal": 50, "discount": 10, "total": 40}


def test_promo_applies_fixed_discount():
    result = applyPromoCode(30, "FIXED5", PROMOS, today=date(2025, 1, 1))
    assert result["total"] == 25


def test_promo_accepts_order_at_minimum():
    assert applyPromoCode(15, "PERCENT20", PROMOS, today=date(2025, 1, 1))["total"] == 12


def test_promo_rejects_order_below_minimum():
    with pytest.raises(PricingError, match="minimum"):
        applyPromoCode(14.99, "PERCENT20", PROMOS, today=date(2025, 1, 1))


def test_promo_rejects_expired_code():
    with pytest.raises(PricingError, match="expired"):
        applyPromoCode(30, "EXPIRED", PROMOS, today=date(2025, 1, 1))


def test_promo_rejects_unknown_code_with_not_found_status():
    with pytest.raises(PricingError) as error:
        applyPromoCode(30, "UNKNOWN", PROMOS, today=date(2025, 1, 1))
    assert error.value.status_code == 404


def test_promo_discounts_never_make_total_negative():
    fixed = applyPromoCode(5, "FIXED5", PROMOS, today=date(2025, 1, 1))
    promos = [{"code": "FREE", "type": "percentage", "value": 100, "minOrder": 0, "expiresAt": "2099-12-31"}]
    percentage = applyPromoCode(20, "FREE", promos, today=date(2025, 1, 1))
    assert fixed["total"] == 0
    assert fixed["discount"] == 5
    assert percentage["total"] == 0


def test_missing_or_empty_promo_code_keeps_subtotal_unchanged():
    for code in (None, ""):
        result = applyPromoCode(12.5, code, PROMOS, today=date(2025, 1, 1))
        assert result["discount"] == 0
        assert result["total"] == 12.5


def test_promo_expiring_today_remains_valid():
    promos = [{"code": "TODAY", "type": "fixed", "value": 1, "minOrder": 0, "expiresAt": "2025-01-01"}]
    assert applyPromoCode(10, "TODAY", promos, today=date(2025, 1, 1))["total"] == 9


def test_promo_rejects_negative_subtotal():
    with pytest.raises(PricingError, match="non-negative"):
        applyPromoCode(-1, "", PROMOS, today=date(2025, 1, 1))


def test_surge_is_normal_on_tuesday_afternoon():
    assert calculateSurge(15, "tuesday") == 1.0


def test_surge_applies_lunch_multiplier():
    assert calculateSurge(12.5, "wednesday") == 1.3


def test_surge_applies_weekday_dinner_multiplier():
    assert calculateSurge(20, "thursday") == 1.5


def test_surge_applies_friday_evening_multiplier():
    assert calculateSurge(21, "friday") == 1.8


def test_surge_applies_sunday_multiplier_during_opening_hours():
    assert calculateSurge(14, "sunday") == 1.2


def test_surge_applies_dinner_at_seven_boundary():
    assert calculateSurge(19, "monday") == 1.5


def test_surge_closes_at_ten_pm():
    assert calculateSurge(22, "friday") == 0


def test_surge_opens_at_ten_am():
    assert calculateSurge(10, "tuesday") == 1.0


PIZZA_ORDER = [{"name": "Pizza", "price": 12.5, "quantity": 2}]


def test_order_total_calculates_subtotal_delivery_and_total():
    result = calculateOrderTotal(PIZZA_ORDER, 5, 2, hour=15, dayOfWeek="tuesday")
    assert result == {"subtotal": 25, "discount": 0, "deliveryFee": 3, "surge": 1.0, "total": 28}


def test_order_total_applies_percentage_promo():
    result = calculateOrderTotal(PIZZA_ORDER, 5, 2, "BIENVENUE20", 15, "tuesday")
    assert result["discount"] == 5
    assert result["total"] == 23


def test_order_total_applies_friday_surge_only_to_delivery():
    result = calculateOrderTotal(PIZZA_ORDER, 5, 2, hour=20, dayOfWeek="friday")
    assert result["subtotal"] == 25
    assert result["deliveryFee"] == 5.4
    assert result["total"] == 30.4


def test_order_total_rejects_empty_cart():
    with pytest.raises(PricingError, match="non-empty"):
        calculateOrderTotal([], 5, 2)


def test_order_total_rejects_zero_quantity():
    with pytest.raises(PricingError, match="quantity"):
        calculateOrderTotal([{"name": "Pizza", "price": 12.5, "quantity": 0}], 5, 2)


def test_order_total_rejects_negative_item_price():
    with pytest.raises(PricingError, match="price"):
        calculateOrderTotal([{"name": "Pizza", "price": -1, "quantity": 1}], 5, 2)


def test_order_total_rejects_closed_hours():
    with pytest.raises(PricingError, match="closed"):
        calculateOrderTotal(PIZZA_ORDER, 5, 2, hour=23, dayOfWeek="tuesday")


def test_order_total_rejects_out_of_zone_distance():
    with pytest.raises(PricingError, match="10 km"):
        calculateOrderTotal(PIZZA_ORDER, 15, 2)


def test_order_total_has_required_fields_and_zero_discount_without_promo():
    result = calculateOrderTotal(PIZZA_ORDER, 5, 2)
    assert set(result) == {"subtotal", "discount", "deliveryFee", "surge", "total"}
    assert result["discount"] == 0


def test_order_total_rejects_expired_promo():
    with pytest.raises(PricingError, match="expired"):
        calculateOrderTotal(PIZZA_ORDER, 5, 2, "EXPIRE")
