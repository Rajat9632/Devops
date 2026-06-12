"""Tests for the calculator module."""

# pyrefly: ignore [missing-import]
import pytest
from app.calculator import Calculator

def test_calculator_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_calculator_subtract():
    calc = Calculator()
    assert calc.subtract(10, 4) == 6

def test_calculator_multiply():
    calc = Calculator()
    assert calc.multiply(3, 4) == 12

def test_calculator_divide():
    calc = Calculator()
    assert calc.divide(10, 2) == 5

def test_calculator_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)
