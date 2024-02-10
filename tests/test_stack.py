import pytest

from pyrpn import stack


def test_stack_init():
    tmp_stack = stack.Stack()
    assert tmp_stack is not None


def test_stack_element():
    tmp_stack_element = stack.StackElement()
    assert tmp_stack_element is not None


def test_basic_stack_functions():
    tmp_stack = stack.Stack()
    tmp_stack.push_back(stack.StackElement())
    assert len(tmp_stack) == 1

    with pytest.raises(AttributeError, match="Invalid argument"):
        tmp_stack.push_back(1)  # pyright: ignore[reportGeneralTypeIssues]
