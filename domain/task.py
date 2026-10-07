"""Entidad Task."""

from __future__ import annotations

from datetime import date


class Task:
    """Tarea de un proyecto. Vive en pendientes o en historial."""

    # Complejidad: O(1)
    def __init__(
        self,
        task_id: str,
        title: str,
        description: str,
        estimation: float,
        due_date: date,
    ) -> None:
        self.task_id = task_id
        self.title = title
        self.description = description
        self.estimation = estimation
        self.due_date = due_date

    # Complejidad: O(1)
    def __str__(self) -> str:
        return f"{self.task_id} - {self.title}"
