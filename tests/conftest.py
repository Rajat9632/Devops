"""Pytest fixtures and configuration."""

import pytest

from app.user import User
from app.payment import Payment


@pytest.fixture
def sample_user() -> User:
    """Return a sample user fixture."""
    return User(user_id=1, name="Alice", email="alice@example.com")


@pytest.fixture
def sample_payment() -> Payment:
    """Return a sample payment fixture."""
    return Payment(payment_id="pay_001", amount=100.0)
