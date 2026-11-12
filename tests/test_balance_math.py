from decimal import Decimal
from app.services.balance_service import BalanceService


def test_amount_to_minor_units():
    assert BalanceService._to_minor_units(Decimal("12.34")) == 1234


def test_amount_rounds_to_minor_unit():
    assert BalanceService._to_minor_units(Decimal("10.999")) == 1100
