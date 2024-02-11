import pytest

from pyrpn import stack


def test_stack_init():
    temp_stack = stack.Stack()
    assert temp_stack is not None


def test_stack_element():
    temp_stack_element = stack.StackElement()
    assert temp_stack_element is not None


def test_basic_stack_functions():
    temp_stack = stack.Stack()
    temp_stack.push_back(stack.StackElement())
    assert len(temp_stack) == 1

    with pytest.raises(AttributeError, match="Invalid argument [(]1[)]"):
        temp_stack.push_back(1)  # pyright: ignore[reportGeneralTypeIssues]
    with pytest.raises(AttributeError, match="Invalid argument [(]Robert[)]"):
        temp_stack.push_back(
            "Robert"  # pyright: ignore[reportGeneralTypeIssues]
        )
    assert str(temp_stack) == '["StackElement" ]'

    with pytest.raises(AttributeError, match="Invalid argument [(]1[)]"):
        temp_stack.push_front(1)  # pyright: ignore[reportGeneralTypeIssues]
    with pytest.raises(AttributeError, match="Invalid argument [(]Robert[)]"):
        temp_stack.push_front(
            "Robert"  # pyright: ignore[reportGeneralTypeIssues]
        )
    temp_stack.push_front(stack.StackElement())
    assert str(temp_stack) == '["StackElement", "StackElement" ]'


def test_stack_number_element():
    temp_stack = stack.Stack()
    temp_stack.push_back(stack.StackNumberElement(1))
    assert str(temp_stack == "[1.0 ]")
    temp_stack.push_back(stack.StackNumberElement(1.1))
    assert len(temp_stack) == 2
    assert str(temp_stack == "[1.0, 1.1 ]")
    temp_element = stack.StackNumberElement(2.5)
    assert str(temp_element) == "2.5"
    temp_stack.push_back(temp_element)
    assert len(temp_stack) == 3
    assert str(temp_stack) == "[1.0, 1.1, 2.5 ]"
    temp_stack.push_back(stack.StackNumberElement(pow(10.5, 100)))
    assert len(temp_stack) == 4
    assert str(temp_stack) == "[1.0, 1.1, 2.5, 1.3150125784630346e+102 ]"
    temp_stack.push_front(stack.StackNumberElement(1.0 / 4.0))
    assert len(temp_stack) == 5
    assert str(temp_stack) == "[0.25, 1.0, 1.1, 2.5, 1.3150125784630346e+102 ]"


def test_stack_clear_function():
    temp_stack = stack.Stack()
    assert len(temp_stack) == 0
    temp_stack.push_back(stack.StackNumberElement(1.5))
    temp_stack.push_back(stack.StackNumberElement(2.5))
    temp_stack.push_back(stack.StackNumberElement(3.5))
    assert len(temp_stack) == 3
    temp_stack.clear()
    assert len(temp_stack) == 0
    assert str(temp_stack) == "[ ]"


def test_stack_peek_functions():
    temp_stack = stack.Stack()
    assert len(temp_stack) == 0
    temp_stack.push_back(stack.StackNumberElement(1.5))
    temp_stack.push_back(stack.StackNumberElement(2.5))
    temp_stack.push_back(stack.StackNumberElement(3.5))
    front_element = temp_stack.peek_front()
    back_element = temp_stack.peek_back()
    assert str(front_element) == "1.5"
    assert str(back_element) == "3.5"
    temp_stack.pop_front()
    temp_stack.pop_front()
    temp_stack.pop_front()
    assert len(temp_stack) == 0
    with pytest.raises(IndexError, match="peek on empty stack"):
        temp_stack.peek_front()
    with pytest.raises(IndexError, match="peek on empty stack"):
        temp_stack.peek_back()


def test_stack_pop_functions():
    temp_stack = stack.Stack()
    assert str(temp_stack) == "[ ]"
    temp_stack.push_back(stack.StackNumberElement(1.5))
    temp_stack.push_back(stack.StackNumberElement(2.5))
    temp_stack.push_back(stack.StackNumberElement(3.5))

    stack_element = temp_stack.pop_front()
    assert isinstance(stack_element, stack.StackElement)
    assert str(stack_element) == "1.5"
    assert str(temp_stack) == "[2.5, 3.5 ]"
    assert len(temp_stack) == 2
    stack_element = temp_stack.pop_back()
    assert isinstance(stack_element, stack.StackElement)
    assert str(stack_element) == "3.5"
    assert str(temp_stack) == "[2.5 ]"
    assert len(temp_stack) == 1
    stack_element = temp_stack.pop_back()
    assert isinstance(stack_element, stack.StackElement)
    assert str(stack_element) == "2.5"
    assert str(temp_stack) == "[ ]"
    assert len(temp_stack) == 0

    with pytest.raises(IndexError, match="pop from empty stack"):
        temp_stack.pop_front()
    with pytest.raises(IndexError, match="pop from empty stack"):
        temp_stack.pop_back()
