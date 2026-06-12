"""Pytest fixtures and configuration."""

import pytest

from app.user import User
from app.payment import Payment
from app.order import Order
from app.inventory import Inventory


@pytest.fixture
def sample_user() -> User:
    """Return a sample user fixture."""
    return User(user_id=1, name="Alice", email="alice@example.com")


@pytest.fixture
def sample_payment() -> Payment:
    """Return a sample payment fixture."""
    return Payment(payment_id="pay_001", amount=100.0)


@pytest.fixture
def sample_order() -> Order:
    """Return a sample order fixture."""
    return Order(order_id=1, item="Laptop")


@pytest.fixture
def sample_inventory() -> Inventory:
    """Return a sample inventory fixture."""
    inv = Inventory()
    inv.add_item("Keyboard", 10)
    return inv
