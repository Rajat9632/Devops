"""Tests for the calculator module."""

# pyrefly: ignore [missing-import]
import pytest
from app.calculator import Calculator


@pytest.mark.smoke
def test_calculator_add():
    """Test addition operation."""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0

