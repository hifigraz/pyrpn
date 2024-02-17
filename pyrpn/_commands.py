"""Builtin Calculator commands go into this module."""

from typing import Dict

from ._stack import Stack, StackNumberElement


class CalculatorCommand:
    """Command Pattern base class for Calculator."""

    COMMAND_NAME = "bogus"

    def __init__(
        self, stack: Stack, arguments: Dict[str, float | int | str] = {}
    ):
        """Initialize object."""
        self._stack = stack
        self._undo_stack = Stack()
        self._done = False
        self._arguments = arguments

    def _prepare(self):
        """Prepare needed elements. and do validity checks."""

    def _do(self):
        """Implement the command."""
        raise NotImplementedError(
            "CalculatorCommand base class not implemented."
        )

    def _undo(self):
        """Implement undo command."""
        raise NotImplementedError(
            "CalculatorCommand base class not implemented."
        )

    def do(self):
        """Execute do."""
        if self._done:
            raise RuntimeError("Command already done.")
        self._prepare()
        self._do()
        self._done = True

    def undo(self):
        """Execute undo."""
        if not self._done:
            raise RuntimeError("Command not done yet.")
        self._undo()
        self._done = False


class PushCommand(CalculatorCommand):
    """Push an float number to the stack."""

    VALUE_KEY = "value"

    def _do(self):
        value = self._arguments[PushCommand.VALUE_KEY]
        if type(value) in [float, int]:
            self._stack.push_top(StackNumberElement(float(value)))
        else:
            raise TypeError(
                "%s value is no float but %s" % (value, type(value))
            )

    def _undo(self):
        self._stack.pop_top()


class PopCommand(CalculatorCommand):
    """Pop an element from the stack."""

    def _prepare(self):
        if len(self._stack) < 1:
            raise ValueError("No element on stack.")

    def _do(self):
        self._undo_stack.push_top(self._stack.pop_top())

    def _undo(self):
        self._stack.push_top(self._undo_stack.pop_top())


class ClearCommand(CalculatorCommand):
    """Clear the entire stack."""

    def _do(self):
        while len(self._stack):
            self._undo_stack.push_top(self._stack.pop_top())

    def _undo(self):
        while len(self._undo_stack):
            self._stack.push_top(self._undo_stack.pop_top())


class CalculatorCommandTwoElements(CalculatorCommand):
    """Base class for command, which need two elements on the stack."""

    def __init__(self, stack):
        """Construct the two Elements command."""
        super().__init__(stack)
        self._a: StackNumberElement = StackNumberElement(0)
        self._b: StackNumberElement = StackNumberElement(0)

    def _prepare(self):
        if len(self._stack) < 2:
            raise ValueError("Too less elements on stack.")
        temp_element = self._stack.pop_top()
        if isinstance(temp_element, StackNumberElement):
            self._b = temp_element
            self._undo_stack.push_top(self._b)
        else:
            self._stack.push_top(temp_element)
            raise ValueError(
                "%s is not of type StackNumberElement." % temp_element
            )
        temp_element = self._stack.pop_top()
        if isinstance(temp_element, StackNumberElement):
            self._a = temp_element
            self._undo_stack.push_top(self._a)
        else:
            self._stack.push_top(temp_element)
            self._stack.push_top(self._undo_stack.pop_top())
            raise ValueError(
                "%s is not of type StackNumberElement." % temp_element
            )

    def _undo(self):
        """Undo command."""
        self._stack.pop_top()
        self._stack.push_top(self._undo_stack.pop_top())
        self._stack.push_top(self._undo_stack.pop_top())


class SwapCommand(CalculatorCommandTwoElements):
    """Swap Command."""

    COMMAND_NAME = "swap"

    def _do(self):
        self._stack.push_top(self._b)
        self._stack.push_top(self._a)

    def _undo(self):
        a = self._stack.pop_top()
        b = self._stack.pop_top()
        self._stack.push_top(a)
        self._stack.push_top(b)


class CalculatorCommandAdd(CalculatorCommandTwoElements):
    """Command Add."""

    COMMAND_NAME = "add"

    def _do(self):
        """Execute command."""
        self._stack.push_top(self._a + self._b)


class CalculatorCommandSub(CalculatorCommandTwoElements):
    """Command Sub."""

    COMMAND_NAME = "sub"

    def _do(self):
        self._stack.push_top(self._a - self._b)


class CalculatorCommandMultiply(CalculatorCommandTwoElements):
    """Command Multiply."""

    COMMAND_NAME = "multiply"

    def _do(self):
        self._stack.push_top(self._a * self._b)


class CalculatorCommandDivide(CalculatorCommandTwoElements):
    """Command Divide."""

    COMMAND_NAME = "divide"

    def _do(self):
        self._stack.push_top(self._a / self._b)
