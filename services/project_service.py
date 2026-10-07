"""Servicio de proyectos: crear, buscar, editar, eliminar y listar."""

from __future__ import annotations

from core.deque import Deque
from core.exceptions import DuplicateCodeError, EntityNotFoundError, ValidationError
from domain.project import Project
from factories.project_factory import ProjectFactory


class ProjectService:
    """Operaciones de negocio sobre el Deque principal de proyectos."""

    # Complejidad: O(1)
    def __init__(self, projects: Deque, factory: ProjectFactory) -> None:
        self._projects = projects
        self._factory = factory

    # Complejidad: O(n)
    def exists(self, code: str) -> bool:
        return self._projects.contains(lambda project: project.code == code)

    # Complejidad: O(n)
    def find_by_code(self, code: str) -> Project | None:
        return self._projects.find(lambda project: project.code == code)

    # Complejidad: O(n)
    def require(self, code: str) -> Project:
        project = self.find_by_code(code)
        if project is None:
            raise EntityNotFoundError(f"No existe un proyecto con codigo '{code}'.")
        return project

    # Complejidad: O(n)
    def create(self, code: str, name: str, description: str, start_date: str) -> Project:
        if self.exists(code):
            raise DuplicateCodeError(f"El codigo '{code}' ya existe.")
        project = self._factory.create(code, name, description, start_date)
        self._projects.insert_rear(project)
        return project

    # Complejidad: O(n)
    def update(self, code: str, name: str, description: str) -> Project:
        project = self.require(code)
        project.name = name
        project.description = description
        return project

    # Complejidad: O(n)
    def delete(self, code: str) -> Project:
        project = self.require(code)
        if not project.tasks.is_empty() or not project.history.is_empty():
            raise ValidationError(
                "No se puede eliminar un proyecto con tareas o historial."
            )
        self._projects.remove(lambda item: item.code == code)
        return project

    # Complejidad: O(n)
    def iter_projects(self, reverse: bool = False):
        if reverse:
            yield from self._projects.iter_reverse()
        else:
            yield from self._projects

    # Complejidad: O(1)
    def count(self) -> int:
        return self._projects.size
