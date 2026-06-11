"""Tests for the payment module."""

# pyrefly: ignore [missing-import]
import pytest

from app.payment import Payment, PaymentStatus, calculate_tax, calculate_total


@pytest.mark.smoke
def test_payment_creation() -> None:
    """Smoke test: ensure a payment can be created."""
    payment = Payment("pay_002", 50.0, "eur")
    assert payment.amount == 50.0
    assert payment.currency == "EUR"
    assert payment.status == PaymentStatus.PENDING


@pytest.mark.regression
def test_payment_process(sample_payment: Payment) -> None:
    """Regression test: payment processing changes status."""
    sample_payment.process()
    assert sample_payment.status == PaymentStatus.COMPLETED


@pytest.mark.regression
def test_payment_refund(sample_payment: Payment) -> None:
    """Regression test: refund logic."""
    sample_payment.process()
    sample_payment.refund()
    assert sample_payment.status == PaymentStatus.REFUNDED


def test_payment_refund_not_completed(sample_payment: Payment) -> None:
    """Test that refunding a non-completed payment fails."""
    with pytest.raises(RuntimeError):
        sample_payment.refund()


def test_payment_negative_amount() -> None:
    """Test that negative amount raises ValueError."""
    with pytest.raises(ValueError):
        Payment("pay_003", -10.0)


@pytest.mark.smoke
def test_calculate_tax() -> None:
    """Smoke test: tax calculation."""
    assert calculate_tax(100.0) == 8.0
    assert calculate_tax(100.0, 0.10) == 10.0


def test_calculate_tax_negative_amount() -> None:
    """Test that negative amount for tax raises ValueError."""
    with pytest.raises(ValueError):
        calculate_tax(-5.0)


@pytest.mark.smoke
def test_calculate_total() -> None:
    """Smoke test: total calculation with default tax."""
    assert calculate_total(100.0) == 108.0


def test_payment_to_dict(sample_payment: Payment) -> None:
    """Test payment serialization."""
    sample_payment.process()
    data = sample_payment.to_dict()
    assert data["payment_id"] == "pay_001"
    assert data["status"] == "completed"
