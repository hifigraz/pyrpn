"""Test the calculator class."""

from pytest import raises

import pyrpn


def test_calculator_instance():
    """Test the instantiation of the calculator class."""
    calculator = pyrpn.calculator.Calculator()
    assert calculator


def test_calculator_stack_iterator():
    """Test the iterator."""
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


def test_command_base_class():
    """Test the Base command class."""
    stack = pyrpn.stack.Stack()
    base_command = pyrpn.calculator.CalculatorCommand(stack)
    assert base_command
    assert str(stack) == "[ ]"
    with raises(
        NotImplementedError,
        match="CalculatorCommand base class not implemented.",
    ):
        base_command.do()
    assert str(stack) == "[ ]"
    stack.push_top(pyrpn.stack.StackNumberElement(1))
    with raises(
        NotImplementedError,
        match="CalculatorCommand base class not implemented.",
    ):
        base_command.do()
    assert str(stack) == "[1.0 ]"


def test_command_two_elements():
    """Test the two elements base class error cases."""
    stack = pyrpn.stack.Stack()
    stack.push_top(pyrpn.stack.StackElement())
    stack.push_top(pyrpn.stack.StackNumberElement(1))
    assert str(stack) == '[1.0, "StackElement" ]'
    with raises(
        ValueError, match='"StackElement" is not of type StackNumberElement.'
    ):
        two_command = pyrpn.calculator.CalculatorCommandTwoElements(stack)
        two_command.do()
    assert str(stack) == '[1.0, "StackElement" ]'

    stack.clear()
    stack.push_top(pyrpn.stack.StackNumberElement(1))
    stack.push_top(pyrpn.stack.StackElement())
    assert str(stack) == '["StackElement", 1.0 ]'
    with raises(
        ValueError, match='"StackElement" is not of type StackNumberElement.'
    ):
        two_command = pyrpn.calculator.CalculatorCommandTwoElements(stack)
        two_command.do()
    assert str(stack) == '["StackElement", 1.0 ]'


def test_command_add_class():
    """Test the Add command."""
    stack = pyrpn.stack.Stack()
    stack.push_top(pyrpn.stack.StackNumberElement(1.5))
    stack.push_top(pyrpn.stack.StackNumberElement(2.1))
    assert str(stack) == "[2.1, 1.5 ]"
    add_command = pyrpn.calculator.CalculatorCommandAdd(stack)
    add_command.do()
    assert str(stack) == "[3.6 ]"
    add_command.undo()
    assert str(stack) == "[2.1, 1.5 ]"


def test_command_sub_class():
    """Test the Subtraction command."""
    stack = pyrpn.stack.Stack()
    stack.push_top(pyrpn.stack.StackNumberElement(1.5))
    stack.push_top(pyrpn.stack.StackNumberElement(2.1))
    assert str(stack) == "[2.1, 1.5 ]"
    add_command = pyrpn.calculator.CalculatorCommandSub(stack)
    add_command.do()
    assert abs(stack[0]._data - -0.6) < 0.000001  # type:ignore
    add_command.undo()
    assert str(stack) == "[2.1, 1.5 ]"


def test_command_multiply_class():
    """Test the multiplication."""
    stack = pyrpn.stack.Stack()
    stack.push_top(pyrpn.stack.StackNumberElement(2.5))
    stack.push_top(pyrpn.stack.StackNumberElement(2.0))
    assert str(stack) == "[2.0, 2.5 ]"
    multiply_command = pyrpn.calculator.CalculatorCommandMultiply(stack)
    multiply_command.do()
    assert str(stack) == "[5.0 ]"
    multiply_command.undo()
    assert str(stack) == "[2.0, 2.5 ]"


def test_command_divide():
    """Test the division."""
    stack = pyrpn.stack.Stack()
    stack.push_top(pyrpn.stack.StackNumberElement(5.0))
    stack.push_top(pyrpn.stack.StackNumberElement(2.0))
    assert str(stack) == "[2.0, 5.0 ]"
    divide_command = pyrpn.calculator.CalculatorCommandDivide(stack)
    divide_command.do()
    assert str(stack) == "[2.5 ]"
    divide_command.undo()
    assert str(stack) == "[2.0, 5.0 ]"
