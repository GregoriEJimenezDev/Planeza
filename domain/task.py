from __future__ import annotations


class Task:
    # Complejidad: O(1)
    def __init__(
        self,
        task_id: str,
        title: str,
        description: str,
        priority: str,
        estimation: float,
    ) -> None:
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.estimation = estimation

    # Complejidad: O(1)
    def __str__(self) -> str:
        return f"{self.task_id} - {self.title}"
