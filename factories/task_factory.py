"""Fabrica de tareas validadas."""

from __future__ import annotations

from domain.task import Task
from factories import Validator


class TaskFactory:
    """Crea tareas validadas."""

    # Complejidad: O(1)
    def __init__(
        self,
        id_validator: Validator,
        title_validator: Validator,
        description_validator: Validator,
        estimation_validator: Validator,
        date_validator: Validator,
    ) -> None:
        self.id_validator = id_validator
        self.title_validator = title_validator
        self.description_validator = description_validator
        self.estimation_validator = estimation_validator
        self.date_validator = date_validator

    # Complejidad: O(n)
    def create(
        self,
        task_id: str,
        title: str,
        description: str,
        estimation: str,
        due_date: str,
    ) -> Task:
        valid_id = self.id_validator.validate(task_id)
        valid_title = self.title_validator.validate(title)
        valid_description = self.description_validator.validate(description)
        valid_estimation = self.estimation_validator.validate(estimation)
        valid_date = self.date_validator.validate(due_date)
        return Task(valid_id, valid_title, valid_description, valid_estimation, valid_date)
