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


class CalculatorCommand:
    """Command Pattern base class for Calculator."""

    COMMAND_NAME = "bogus"

    def __init__(self, stack: Stack):
        """Initialize object."""
        self._stack = stack
        self._undo_stack = Stack()
        self._done = False

    def _prepare(self):
        """Prepare needed elements. and do validity checks."""
        raise NotImplementedError(
            "CalculatorCommand base class not implemented."
        )

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
        self._prepare()
        self._do()
        self._done = True

    def undo(self):
        """Execute undo."""
        if not self._done:
            raise ValueError("Command not done and cannot be undo.")
        self._undo()
        self._done = False


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
