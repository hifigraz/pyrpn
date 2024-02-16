"""Calculator class."""

import logging

from typing import Dict, List, Set, Type

from ._commands import CalculatorCommand, PushCommand
from ._stack import Stack


class CommandMapping:
    """Mapping keys to commands."""

    def __init__(self, keys: Set[str], command: Type):
        """Construct the mapping."""
        self._keys = keys
        self._command = command

    def _get_keys(self):
        return self._keys

    def _get_command(self):
        return self._command

    keys = property(fget=_get_keys)
    command = property(fget=_get_command)


class Calculator:
    """The calculator class."""

    def __init__(self):
        """Implement the default constructor."""
        self._stack = Stack()
        self._commands: Dict[str, Type] = {}
        self._undo_commands: List[CalculatorCommand] = []
        self._redo_commands: List[CalculatorCommand] = []

    def register_command(self, mapping: CommandMapping) -> None:
        """Map new command to calculator."""
        for key in mapping.keys:
            if key in self._commands:
                raise ValueError("%s already registered as key." % key)
        for key in mapping.keys:
            self._commands[key] = mapping.command

    def registered_key(self, key: str) -> bool:
        """Check if the given key is a registered one."""
        return key in self._commands

    def __add__(self, other: float | int | str) -> "Calculator":
        """Add elements to the calculator."""
        command: None | CalculatorCommand = None
        if other in self.keys:
            command = self._commands[str(other)](self._stack)
        elif type(other) is float or type(other) is int:
            command = PushCommand(self._stack, {PushCommand.VALUE_KEY: other})
        elif type(other) is str:
            try:
                number = float(other)
                command = PushCommand(
                    self._stack, {PushCommand.VALUE_KEY: number}
                )

            except Exception:
                logging.error("Other %s not supported" % other)
                raise NotImplementedError(
                    "Pushing strings to the stack is not yet supported."
                )
        if isinstance(command, CalculatorCommand):
            command.do()
            self._undo_commands.append(command)
            self._redo_commands.clear()
        else:
            raise RuntimeError(
                "operand is of unsupported type %s" % type(other)
            )
        return self

    def undo(self) -> None:
        """Undo command."""
        if len(self._undo_commands):
            command = self._undo_commands.pop()
            command.undo()
            self._redo_commands.append(command)

    def redo(self) -> None:
        """Redo command."""
        if len(self._redo_commands):
            command = self._redo_commands.pop()
            command.do()
            self._undo_commands.append(command)

    def _get_stack(self):
        return self._stack

    def _get_keys(self):
        return self._commands.keys()

    keys = property(fget=_get_keys)
    stack = property(
        _get_stack,
    )
