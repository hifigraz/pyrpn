"""Calculator class."""

from ._stack import Stack, StackNumberElement


class Calculator:
    """The calculator class."""

    def __init__(self):
        """Implement the default constructor."""
        self._stack = Stack()

    def _get_stack(self):
        return self._stack

    stack = property(
        _get_stack,
    )

    def __add__(self, other: float | int | str) -> "Calculator":
        """Add elements to the calculator."""
        self._stack.push_top(StackNumberElement(float(other)))
        return self
