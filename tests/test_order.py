"""Tests for order module."""

# pyrefly: ignore [missing-import]
import pytest
from app.order import Order

@pytest.mark.smoke
def test_order_creation():
    order = Order(1, "Laptop")
    assert order.item == "Laptop"
    assert order.status == "Pending"

@pytest.mark.regression
def test_order_completion():
    order = Order(2, "Phone")
    order.complete()
    assert order.status == "Completed"
