"""Factory methods for pyrpn."""

from ._calculator import Calculator, CommandMapping
from ._commands import (
    CalculatorCommandAdd,
    CalculatorCommandDivide,
    CalculatorCommandMultiply,
    CalculatorCommandSub,
    ClearCommand,
    PopCommand,
    SwapCommand,
)


def create_basic_arithmetic_calculator() -> Calculator:
    """Generate a simple calculator configured for basic arithmetic."""
    calculator: Calculator = Calculator()
    calculator.register_command(
        CommandMapping({"+", "plus"}, CalculatorCommandAdd)
    )
    calculator.register_command(
        CommandMapping({"-", "substract"}, CalculatorCommandSub)
    )
    calculator.register_command(
        CommandMapping({"*", "multiply"}, CalculatorCommandMultiply)
    )
    calculator.register_command(
        CommandMapping({"/", "divide"}, CalculatorCommandDivide)
    )
    calculator.register_command(
        CommandMapping({"pop", "POP", "Pop"}, PopCommand)
    )
    calculator.register_command(
        CommandMapping({"clear", "Clear", "CLEAR"}, ClearCommand)
    )
    calculator.register_command(
        CommandMapping({"swap", "Swap", "SWAP"}, SwapCommand)
    )
    return calculator
