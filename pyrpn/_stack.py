from typing import List


class StackElement:
    def __str__(self) -> str:
        return '"StackElement"'


class StackNumberElement(StackElement):
    def __init__(self, number: StackElement | int | float):
        if type(number) is int:
            self._data = float(number)
        elif type(number) is float:
            self._data = number
        elif isinstance(number, StackNumberElement):
            self.data = number._data
        else:
            raise AttributeError("Invalid argument (%s)" % str(number))

    def __str__(self) -> str:
        return str(self._data)


class Stack:
    def __init__(self):
        self._data: List[StackElement] = []

    def clear(self):
        self._data.clear()

    def push_back(self, stack_element: StackElement) -> None:
        if not isinstance(stack_element, StackElement):
            raise AttributeError("Invalid argument (%s)" % str(stack_element))
        self._data.append(stack_element)

    def push_front(self, stack_element: StackElement) -> None:
        if not isinstance(stack_element, StackElement):
            raise AttributeError("Invalid argument (%s)" % str(stack_element))
        self._data = [stack_element] + self._data

    def peek_front(self) -> StackElement:
        try:
            return self._data[0]
        except IndexError:
            raise IndexError("peek on empty stack")

    def peek_back(self) -> StackElement:
        try:
            return self._data[-1]
        except IndexError:
            raise IndexError("peek on empty stack")

    def pop_front(self) -> StackElement:
        try:
            return self._data.pop(0)
        except IndexError:
            raise IndexError("pop from empty stack")

    def pop_back(self) -> StackElement:
        try:
            return self._data.pop(-1)
        except IndexError:
            raise IndexError("pop from empty stack")

    def __len__(self) -> int:
        return len(self._data)

    def __str__(self) -> str:
        return_value = "[%s ]"
        return_value = return_value % ", ".join(
            map(lambda x: str(x), self._data)
        )
        return return_value
