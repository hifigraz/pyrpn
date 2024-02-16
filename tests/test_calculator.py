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
    base_command = pyrpn.commands.CalculatorCommand(stack)
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
        two_command = pyrpn.commands.CalculatorCommandTwoElements(stack)
        two_command.do()
    assert str(stack) == '[1.0, "StackElement" ]'

    stack.clear()
    stack.push_top(pyrpn.stack.StackNumberElement(1))
    stack.push_top(pyrpn.stack.StackElement())
    assert str(stack) == '["StackElement", 1.0 ]'
    with raises(
        ValueError, match='"StackElement" is not of type StackNumberElement.'
    ):
        two_command = pyrpn.commands.CalculatorCommandTwoElements(stack)
        two_command.do()
    assert str(stack) == '["StackElement", 1.0 ]'


def test_command_add_class():
    """Test the Add command."""
    stack = pyrpn.stack.Stack()
    stack.push_top(pyrpn.stack.StackNumberElement(1.5))
    stack.push_top(pyrpn.stack.StackNumberElement(2.1))
    assert str(stack) == "[2.1, 1.5 ]"
    add_command = pyrpn.commands.CalculatorCommandAdd(stack)
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
    add_command = pyrpn.commands.CalculatorCommandSub(stack)
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
    multiply_command = pyrpn.commands.CalculatorCommandMultiply(stack)
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
    divide_command = pyrpn.commands.CalculatorCommandDivide(stack)
    divide_command.do()
    assert str(stack) == "[2.5 ]"
    divide_command.undo()
    assert str(stack) == "[2.0, 5.0 ]"


def test_push_pop():
    """Test the push and pop commands."""
    stack = pyrpn.stack.Stack()
    push_command = pyrpn.commands.PushCommand(
        stack, {pyrpn.commands.PushCommand.VALUE_KEY: 2}
    )
    assert str(stack) == "[ ]"
    with raises(RuntimeError, match="Command not done yet."):
        push_command.undo()
    push_command.do()
    assert str(stack) == "[2.0 ]"
    push_command.undo()
    assert str(stack) == "[ ]"
    push_command.do()
    assert str(stack) == "[2.0 ]"
    pop_command = pyrpn.commands.PopCommand(stack)
    pop_command.do()
    with raises(RuntimeError, match="Command already done."):
        pop_command.do()
    assert str(stack) == "[ ]"
    pop_command.undo()
    assert str(stack) == "[2.0 ]"
    pop_command.do()
    with raises(RuntimeError, match="Command already done."):
        pop_command.do()
    pop_command = pyrpn.commands.PopCommand(stack)
    with raises(ValueError, match="No element on stack."):
        pop_command.do()


def test_calculator_basics():
    """Test basic functionality of calculator."""
    calculator = pyrpn.calculator.Calculator()
    mapping = pyrpn.calculator.CommandMapping(
        {"bogus", "b"}, pyrpn.commands.CalculatorCommand
    )
    assert False is calculator.registered_key("b")
    assert False is calculator.registered_key("bogus")
    calculator.register_command(mapping)
    assert True is calculator.registered_key("b")
    assert True is calculator.registered_key("bogus")
    mapping = pyrpn.calculator.CommandMapping(
        {"bogus"}, pyrpn.commands.CalculatorCommand
    )
    with raises(ValueError, match="bogus already registered as key."):
        calculator.register_command(mapping)
    mapping = pyrpn.calculator.CommandMapping(
        {"b"}, pyrpn.commands.CalculatorCommand
    )
    with raises(ValueError, match="b already registered as key."):
        calculator.register_command(mapping)


def test_calculator_add_sub():
    """Test simple add and sub."""
    calculator = pyrpn.calculator.Calculator()
    calculator.register_command(
        pyrpn.calculator.CommandMapping(
            {"+"}, pyrpn.commands.CalculatorCommandAdd
        )
    )
    calculator.register_command(
        pyrpn.calculator.CommandMapping(
            {"-"}, pyrpn.commands.CalculatorCommandSub
        )
    )
    assert str(calculator.stack) == "[ ]"
    calculator += 6
    calculator += 3
    assert str(calculator.stack) == "[3.0, 6.0 ]"
    calculator += "+"
    assert str(calculator.stack) == "[9.0 ]"
    calculator.undo()
    assert str(calculator.stack) == "[3.0, 6.0 ]"
    calculator.redo()
    assert str(calculator.stack) == "[9.0 ]"
    calculator.undo()
    assert str(calculator.stack) == "[3.0, 6.0 ]"
    calculator += "2"
    assert str(calculator.stack) == "[2.0, 3.0, 6.0 ]"
    calculator += "-"
    assert str(calculator.stack) == "[1.0, 6.0 ]"
    calculator += "+"
    assert str(calculator.stack) == "[7.0 ]"
    calculator.undo()
    calculator.undo()
    assert str(calculator.stack) == "[2.0, 3.0, 6.0 ]"
