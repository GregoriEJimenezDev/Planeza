from __future__ import annotations

from datetime import date

from core.deque import Deque


class Project:
    # Complejidad: O(1)
    def __init__(
        self,
        code: str,
        name: str,
        description: str,
        responsible: str,
        start_date: date,
    ) -> None:
        self.code = code
        self.name = name
        self.description = description
        self.responsible = responsible
        self.start_date = start_date
        self.tasks = Deque()
        self.history = Deque()

    # Complejidad: O(1)
    @property
    def pending_count(self) -> int:
        return self.tasks.size

    # Complejidad: O(1)
    @property
    def processed_count(self) -> int:
        return self.history.size
