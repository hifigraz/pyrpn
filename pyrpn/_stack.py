from collections.abc import Iterator

from typing import List


class StackElement:
    """Implements a element which can be put onto stack."""

    def __str__(self) -> str:
        """Return the string representation of the stack element."""
        return '"StackElement"'


class StackNumberElement(StackElement):
    """Specialization of StackElement supporting numbers on the stack."""

    def __init__(self, number: StackElement | int | float):
        """Implement the constructor of the StackNumberElement.

        * number : Either a number or another StackNumberElement
                   to be used for this stack element
        """
        if type(number) is int:
            self._data = float(number)
        elif type(number) is float:
            self._data = number
        elif isinstance(number, StackNumberElement):
            self.data = number._data
        else:
            raise AttributeError("Invalid argument (%s)" % str(number))

    def __str__(self) -> str:
        """Implement a string representation."""
        return str(self._data)


class Stack:
    """Implement a multi purpose stack for the RPN calculator."""

    def __init__(self):
        """Implement the default constructor."""
        self._data: List[StackElement] = []

    def __len__(self) -> int:
        """Return the number of elements on the stack."""
        return len(self._data)

    def __str__(self) -> str:
        """Return a string representation of the stack."""
        return_value = "[%s ]"
        return_value = return_value % ", ".join(
            map(lambda x: str(x), self._data)
        )
        return return_value

    def __iter__(self) -> Iterator[StackElement]:
        """Create an iterator."""
        return self._data.__iter__()

    def clear(self):
        """Clear every element on the stack."""
        self._data.clear()

    def push_bottom(self, stack_element: StackElement) -> None:
        """
        Push an element to the bottom of the stack.

        - stack_element: the stack element to be pushed.
        """
        if not isinstance(stack_element, StackElement):
            raise AttributeError("Invalid argument (%s)" % str(stack_element))
        self._data.append(stack_element)

    def push_top(self, stack_element: StackElement) -> None:
        """
        Push an element on top of the stack.

        - stack_element: the stack element to be pushed.
        """
        if not isinstance(stack_element, StackElement):
            raise AttributeError("Invalid argument (%s)" % str(stack_element))
        self._data = [stack_element] + self._data

    def peek_top(self) -> StackElement:
        """Take a peek onto the top element of the stack."""
        try:
            return self._data[0]
        except IndexError:
            raise IndexError("peek on empty stack")

    def peek_bottom(self) -> StackElement:
        """Take a peek onto the bottom element of the stack."""
        try:
            return self._data[-1]
        except IndexError:
            raise IndexError("peek on empty stack")

    def pop_top(self) -> StackElement:
        """Remove and return the top element of the stack."""
        try:
            return self._data.pop(0)
        except IndexError:
            raise IndexError("pop from empty stack")

    def pop_bottom(self) -> StackElement:
        """Remove and return the bottom element of the stack."""
        try:
            return self._data.pop(-1)
        except IndexError:
            raise IndexError("pop from empty stack")
