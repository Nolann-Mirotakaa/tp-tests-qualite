import pytest

from src.pricing import PricingError, calculateDeliveryFee, applyPromoCode


def test_delivery_fee_two_kilometers():
    assert calculateDeliveryFee(2, 1) == 2.0


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


def test_delivery_fee_does_not_surcharge_exactly_five_kilograms():
    assert calculateDeliveryFee(3, 5) == 2.0



from datetime import date

from src.pricing import applyPromoCode


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


def test_promo_fixed_discount_never_makes_total_negative():
    result = applyPromoCode(5, "FIXED5", PROMOS, today=date(2025, 1, 1))
    assert result["total"] == 0
    assert result["discount"] == 5


def test_promo_accepts_one_hundred_percent_discount():
    promos = [{"code": "FREE", "type": "percentage", "value": 100, "minOrder": 0, "expiresAt": "2099-12-31"}]
    assert applyPromoCode(20, "FREE", promos, today=date(2025, 1, 1))["total"] == 0


def test_missing_promo_code_keeps_subtotal_unchanged():
    assert applyPromoCode(12.5, None, PROMOS, today=date(2025, 1, 1))["discount"] == 0


def test_empty_promo_code_keeps_subtotal_unchanged():
    assert applyPromoCode(12.5, "", PROMOS, today=date(2025, 1, 1))["total"] == 12.5


def test_promo_expiring_today_remains_valid():
    promos = [{"code": "TODAY", "type": "fixed", "value": 1, "minOrder": 0, "expiresAt": "2025-01-01"}]
    assert applyPromoCode(10, "TODAY", promos, today=date(2025, 1, 1))["total"] == 9


def test_promo_rejects_negative_subtotal():
    with pytest.raises(PricingError, match="non-negative"):
        applyPromoCode(-1, "", PROMOS, today=date(2025, 1, 1))
