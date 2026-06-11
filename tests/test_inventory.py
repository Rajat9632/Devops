"""Tests for the inventory module."""

# pyrefly: ignore [missing-import]
import pytest
from app.inventory import Inventory

@pytest.mark.smoke
def test_inventory_add():
    inv = Inventory()
    inv.add_item("Keyboard", 5)
    assert inv.get_stock("Keyboard") == 5

@pytest.mark.regression
def test_inventory_multiple_adds():
    inv = Inventory()
    inv.add_item("Mouse", 2)
    inv.add_item("Mouse", 3)
    assert inv.get_stock("Mouse") == 5

def test_inventory_empty():
    inv = Inventory()
    assert inv.get_stock("Monitor") == 0
