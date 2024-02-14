"""Test the calculator class."""

import pyrpn


def test_calculator_instance():
    """Test the instantiation of the calculator class."""
    calculator = pyrpn.calculator.Calculator()
    assert calculator


def test_calculator_stack_iterator():
    """Test the iterator"""
    calculator = pyrpn.calculator.Calculator()
    assert len(calculator.stack) == 0


def test_calculator_stack_number_push():
    """Test if pushing a number to stack works."""
    calculator = pyrpn.calculator.Calculator()
    assert len(calculator.stack) == 0
    calculator += 1
    assert len(calculator.stack) == 1
    assert str(calculator.stack) == "[1.0 ]"
    calculator += 1.0
    assert len(calculator.stack) == 2
    assert str(calculator.stack) == "[1.0, 1.0 ]"
    calculator += "1.0"
    assert len(calculator.stack) == 3
    assert str(calculator.stack) == "[1.0, 1.0, 1.0 ]"
    calculator += "0.1e1"
    assert len(calculator.stack) == 4
    assert str(calculator.stack) == "[1.0, 1.0, 1.0, 1.0 ]"
    calculator += "10e-1"
    assert len(calculator.stack) == 5
    assert str(calculator.stack) == "[1.0, 1.0, 1.0, 1.0, 1.0 ]"
