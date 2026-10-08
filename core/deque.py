from __future__ import annotations

from core.deque_node import DequeNode
from core.exceptions import EmptyDequeError


class Deque:
    # Complejidad: O(1)
    def __init__(self) -> None:
        self._front: DequeNode | None = None
        self._rear: DequeNode | None = None
        self._size = 0

    # Complejidad: O(1)
    @property
    def size(self) -> int:
        return self._size

    # Complejidad: O(1)
    def is_empty(self) -> bool:
        return self._size == 0

    # Complejidad: O(1)
    def insert_front(self, data: object) -> None:
        node = DequeNode(data)
        if self._front is None:
            self._front = node
            self._rear = node
        else:
            node.next = self._front
            self._front.prev = node
            self._front = node
        self._size += 1

    # Complejidad: O(1)
    def insert_rear(self, data: object) -> None:
        node = DequeNode(data)
        if self._rear is None:
            self._front = node
            self._rear = node
        else:
            node.prev = self._rear
            self._rear.next = node
            self._rear = node
        self._size += 1

    # Complejidad: O(1)
    def delete_front(self) -> object:
        if self._front is None:
            raise EmptyDequeError("El deque esta vacio.")
        node = self._front
        data = node.data
        self._front = node.next
        if self._front is None:
            self._rear = None
        else:
            self._front.prev = None
        node.next = None
        self._size -= 1
        return data

    # Complejidad: O(1)
    def delete_rear(self) -> object:
        if self._rear is None:
            raise EmptyDequeError("El deque esta vacio.")
        node = self._rear
        data = node.data
        self._rear = node.prev
        if self._rear is None:
            self._front = None
        else:
            self._rear.next = None
        node.prev = None
        self._size -= 1
        return data

    # Complejidad: O(1)
    def get_front(self) -> object:
        if self._front is None:
            raise EmptyDequeError("El deque esta vacio.")
        return self._front.data

    # Complejidad: O(1)
    def get_rear(self) -> object:
        if self._rear is None:
            raise EmptyDequeError("El deque esta vacio.")
        return self._rear.data

    # Complejidad: O(n)
    def __iter__(self):
        current = self._front
        while current is not None:
            yield current.data
            current = current.next

    # Complejidad: O(n)
    def iter_reverse(self):
        current = self._rear
        while current is not None:
            yield current.data
            current = current.prev

    # Complejidad: O(n)
    def find(self, predicate) -> object | None:
        for item in self:
            if predicate(item):
                return item
        return None

    # Complejidad: O(n)
    def contains(self, predicate) -> bool:
        return self.find(predicate) is not None

    # Complejidad: O(n)
    def remove(self, predicate) -> object | None:
        current = self._front
        while current is not None:
            if predicate(current.data):
                data = current.data
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self._front = current.next
                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self._rear = current.prev
                current.next = None
                current.prev = None
                self._size -= 1
                return data
            current = current.next
        return None
