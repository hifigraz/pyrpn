"""This is a module for the main function."""

import os

from ._factory import create_basic_arithmetic_calculator


def simple_calculator() -> int:
    """Execute main function for very simple tui calculator."""
    LINE = 20 * "-"
    CLEAR = chr(27) + "[2J"

    def _print_line():
        print(LINE)

    def _print_stack(stack):
        print("enter >help< for help")
        _print_line()
        for element in reversed(stack):
            print(element)
        _print_line()

    calculator = create_basic_arithmetic_calculator()
    running = True
    error = ""
    help = ""
    while running:
        print(CLEAR)
        _print_stack(calculator.stack)
        if error:
            print("ERROR: %s" % error)
            error = ""
            _print_line()
        if help:
            print(help)
            help = ""
            _print_line()
        print("> ", end="")
        try:
            command = input()
            if command.upper() == "UNDO":
                calculator.undo()
            elif command.upper() == "REDO":
                calculator.redo()
            elif command.upper() == "HELP":
                help = (
                    ""
                    + "valid commands are: %s" % os.linesep
                    + "  help : display this message %s" % os.linesep
                    + "  <num>: a number %s" % os.linesep
                    + "  +    : add top two %s" % os.linesep
                    + "  -    : substract top two %s" % os.linesep
                    + "  *    : multiply top two %s" % os.linesep
                    + "  /    : divide top two %s" % os.linesep
                    + "  clear: clear the stack %s" % os.linesep
                    + "  pop  : pop top element %s" % os.linesep
                    + "  quit : exit calculator %s" % os.linesep
                    + "  redo : redo undone command %s" % os.linesep
                    + "  undo : undo last command %s" % os.linesep
                    + "  swap : swap top two %s" % os.linesep
                    + ""
                )
            elif command.upper() == "QUIT" or command.upper() == "EXIT":
                running = False
            else:
                calculator += command
        except Exception as e:
            error = str(e)

    return 0
