from typing import List


class StackElement:
    pass


class Stack:
    def __init__(self):
        self._data: List[StackElement] = []

    def push_back(self, stack_element: StackElement) -> None:
        if not isinstance(stack_element, StackElement):
            raise AttributeError("Invalid argument")
        self._data.append(stack_element)

    def __len__(self) -> int:
        return len(self._data)
