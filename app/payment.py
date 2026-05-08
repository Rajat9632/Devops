"""Payment module with basic payment processing functions."""

from enum import Enum


class PaymentStatus(Enum):
    """Enumeration of possible payment statuses."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment:
    """Represents a payment transaction."""

    def __init__(self, payment_id: str, amount: float, currency: str = "USD") -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.payment_id = payment_id
        self.amount = amount
        self.currency = currency.upper()
        self.status = PaymentStatus.PENDING

    def process(self) -> None:
        """Process the payment (mock)."""
        self.status = PaymentStatus.COMPLETED

    def refund(self) -> None:
        """Refund the payment."""
        if self.status != PaymentStatus.COMPLETED:
            raise RuntimeError("Only completed payments can be refunded")
        self.status = PaymentStatus.REFUNDED

    def to_dict(self) -> dict:
        """Return payment data as a dictionary."""
        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status.value,
        }


def calculate_tax(amount: float, tax_rate: float = 0.08) -> float:
    """Calculate tax for a given amount."""
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return round(amount * tax_rate, 2)


def calculate_total(amount: float, tax_rate: float = 0.08) -> float:
    """Calculate total amount including tax."""
    return round(amount + calculate_tax(amount, tax_rate), 2)
