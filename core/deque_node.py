"""Nodo doblemente enlazado del Deque."""

from __future__ import annotations


class DequeNode:
    """Nodo doblemente enlazado del Deque."""

    # Complejidad: O(1)
    def __init__(self, data: object) -> None:
        self.data = data
        self.next: DequeNode | None = None
        self.prev: DequeNode | None = None
