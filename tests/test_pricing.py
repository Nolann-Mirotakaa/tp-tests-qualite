import pytest

from src.pricing import PricingError, calculateDeliveryFee


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
