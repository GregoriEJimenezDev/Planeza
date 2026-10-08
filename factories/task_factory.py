from __future__ import annotations

from domain.task import Task
from factories import Validator


class TaskFactory:
    # Complejidad: O(1)
    def __init__(
        self,
        id_validator: Validator,
        title_validator: Validator,
        description_validator: Validator,
        priority_validator: Validator,
        estimation_validator: Validator,
    ) -> None:
        self.id_validator = id_validator
        self.title_validator = title_validator
        self.description_validator = description_validator
        self.priority_validator = priority_validator
        self.estimation_validator = estimation_validator

    # Complejidad: O(n)
    def create(
        self,
        task_id: str,
        title: str,
        description: str,
        priority: str,
        estimation: str,
    ) -> Task:
        valid_id = self.id_validator.validate(task_id)
        valid_title = self.title_validator.validate(title)
        valid_description = self.description_validator.validate(description)
        valid_priority = self.priority_validator.validate(priority)
        valid_estimation = self.estimation_validator.validate(estimation)
        return Task(
            valid_id, valid_title, valid_description, valid_priority, valid_estimation
        )
