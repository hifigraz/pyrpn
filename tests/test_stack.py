"""Implement stack test methods."""

import pytest

from pyrpn import stack


def test_stack_init():
    """Test initialisation of a stack object."""
    temp_stack = stack.Stack()
    assert temp_stack is not None


def test_stack_element():
    """Test a single element to be used with the stack."""
    temp_stack_element = stack.StackElement()
    assert temp_stack_element is not None


def test_basic_stack_functions():
    """Test the basic methods of the stack."""
    temp_stack = stack.Stack()
    temp_stack.push_bottom(stack.StackElement())
    assert len(temp_stack) == 1

    with pytest.raises(AttributeError, match="Invalid argument [(]1[)]"):
        temp_stack.push_bottom(1)  # pyright: ignore[reportGeneralTypeIssues]
    with pytest.raises(AttributeError, match="Invalid argument [(]Robert[)]"):
        temp_stack.push_bottom(
            "Robert"  # pyright: ignore[reportGeneralTypeIssues]
        )
    assert str(temp_stack) == '["StackElement" ]'

    with pytest.raises(AttributeError, match="Invalid argument [(]1[)]"):
        temp_stack.push_top(1)  # pyright: ignore[reportGeneralTypeIssues]
    with pytest.raises(AttributeError, match="Invalid argument [(]Robert[)]"):
        temp_stack.push_top(
            "Robert"  # pyright: ignore[reportGeneralTypeIssues]
        )
    temp_stack.push_top(stack.StackElement())
    assert str(temp_stack) == '["StackElement", "StackElement" ]'


def test_stack_number_element():
    """Test the number element for the stack."""
    temp_stack = stack.Stack()
    temp_stack.push_bottom(stack.StackNumberElement(1))
    assert str(temp_stack == "[1.0 ]")
    temp_stack.push_bottom(stack.StackNumberElement(1.1))
    assert len(temp_stack) == 2
    assert str(temp_stack == "[1.0, 1.1 ]")
    temp_element = stack.StackNumberElement(2.5)
    assert str(temp_element) == "2.5"
    temp_stack.push_bottom(temp_element)
    assert len(temp_stack) == 3
    assert str(temp_stack) == "[1.0, 1.1, 2.5 ]"
    temp_stack.push_bottom(stack.StackNumberElement(pow(10.5, 100)))
    assert len(temp_stack) == 4
    assert str(temp_stack) == "[1.0, 1.1, 2.5, 1.3150125784630346e+102 ]"
    temp_stack.push_top(stack.StackNumberElement(1.0 / 4.0))
    assert len(temp_stack) == 5
    assert str(temp_stack) == "[0.25, 1.0, 1.1, 2.5, 1.3150125784630346e+102 ]"


def test_stack_clear_function():
    """Test clear functionality of the stack."""
    temp_stack = stack.Stack()
    assert len(temp_stack) == 0
    temp_stack.push_bottom(stack.StackNumberElement(1.5))
    temp_stack.push_bottom(stack.StackNumberElement(2.5))
    temp_stack.push_bottom(stack.StackNumberElement(3.5))
    assert len(temp_stack) == 3
    temp_stack.clear()
    assert len(temp_stack) == 0
    assert str(temp_stack) == "[ ]"


def test_stack_peek_functions():
    """Test the peek functions for the stack."""
    temp_stack = stack.Stack()
    assert len(temp_stack) == 0
    temp_stack.push_bottom(stack.StackNumberElement(1.5))
    temp_stack.push_bottom(stack.StackNumberElement(2.5))
    temp_stack.push_bottom(stack.StackNumberElement(3.5))
    top_element = temp_stack.peek_top()
    bottom_element = temp_stack.peek_bottom()
    assert str(top_element) == "1.5"
    assert str(bottom_element) == "3.5"
    temp_stack.pop_top()
    temp_stack.pop_top()
    temp_stack.pop_top()
    assert len(temp_stack) == 0
    with pytest.raises(IndexError, match="peek on empty stack"):
        temp_stack.peek_top()
    with pytest.raises(IndexError, match="peek on empty stack"):
        temp_stack.peek_bottom()


def test_stack_pop_functions():
    """Test the pop functions for the stack."""
    temp_stack = stack.Stack()
    assert str(temp_stack) == "[ ]"
    temp_stack.push_bottom(stack.StackNumberElement(1.5))
    temp_stack.push_bottom(stack.StackNumberElement(2.5))
    temp_stack.push_bottom(stack.StackNumberElement(3.5))

    stack_element = temp_stack.pop_top()
    assert isinstance(stack_element, stack.StackElement)
    assert str(stack_element) == "1.5"
    assert str(temp_stack) == "[2.5, 3.5 ]"
    assert len(temp_stack) == 2
    stack_element = temp_stack.pop_bottom()
    assert isinstance(stack_element, stack.StackElement)
    assert str(stack_element) == "3.5"
    assert str(temp_stack) == "[2.5 ]"
    assert len(temp_stack) == 1
    stack_element = temp_stack.pop_bottom()
    assert isinstance(stack_element, stack.StackElement)
    assert str(stack_element) == "2.5"
    assert str(temp_stack) == "[ ]"
    assert len(temp_stack) == 0

    with pytest.raises(IndexError, match="pop from empty stack"):
        temp_stack.pop_top()
    with pytest.raises(IndexError, match="pop from empty stack"):
        temp_stack.pop_bottom()


def test_stack_iterator_functions():
    """Test the iteration over a stack."""
    temp_stack = stack.Stack()
    assert str(temp_stack) == "[ ]"
    test_elements = [1.5, 2.5, 3.5]
    for i in test_elements:
        temp_stack.push_bottom(stack.StackNumberElement(i))
    index = 0
    for stack_element in temp_stack:
        assert str(test_elements[index]) == str(stack_element)
        index += 1
