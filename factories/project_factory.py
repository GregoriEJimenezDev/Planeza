"""Fabrica de proyectos validados."""

from __future__ import annotations

from domain.project import Project
from factories import Validator


class ProjectFactory:
    """Crea proyectos validados."""

    # Complejidad: O(1)
    def __init__(
        self,
        code_validator: Validator,
        name_validator: Validator,
        description_validator: Validator,
        date_validator: Validator,
    ) -> None:
        self.code_validator = code_validator
        self.name_validator = name_validator
        self.description_validator = description_validator
        self.date_validator = date_validator

    # Complejidad: O(n)
    def create(
        self,
        code: str,
        name: str,
        description: str,
        start_date: str,
    ) -> Project:
        valid_code = self.code_validator.validate(code)
        valid_name = self.name_validator.validate(name)
        valid_description = self.description_validator.validate(description)
        valid_date = self.date_validator.validate(start_date)
        return Project(valid_code, valid_name, valid_description, valid_date)
