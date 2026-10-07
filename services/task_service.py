"""Servicio de tareas: anadir, procesar front/rear y deshacer."""

from __future__ import annotations

from core.exceptions import DuplicateTaskIdError, EmptyDequeError
from domain.project import Project
from domain.task import Task
from factories.task_factory import TaskFactory
from services.project_service import ProjectService


class TaskService:
    """Operaciones de negocio sobre las tareas de un proyecto."""

    # Complejidad: O(1)
    def __init__(self, project_service: ProjectService, factory: TaskFactory) -> None:
        self._project_service = project_service
        self._factory = factory

    # Complejidad: O(n)
    def _ensure_unique_id(self, project: Project, task_id: str) -> None:
        if project.tasks.contains(lambda task: task.task_id == task_id):
            raise DuplicateTaskIdError(
                f"La tarea '{task_id}' ya existe en el proyecto '{project.code}'."
            )
        if project.history.contains(lambda task: task.task_id == task_id):
            raise DuplicateTaskIdError(
                f"La tarea '{task_id}' ya existe en el proyecto '{project.code}'."
            )

    # Complejidad: O(n)
    def add_task(
        self,
        code: str,
        task_id: str,
        title: str,
        description: str,
        estimation: str,
        due_date: str,
    ) -> Task:
        project = self._project_service.require(code)
        self._ensure_unique_id(project, task_id)
        task = self._factory.create(task_id, title, description, estimation, due_date)
        project.tasks.insert_rear(task)
        return task

    # Complejidad: O(n)
    def process_front(self, code: str) -> Task:
        project = self._project_service.require(code)
        if project.tasks.is_empty():
            raise EmptyDequeError("El proyecto no tiene tareas pendientes.")
        task = project.tasks.delete_front()
        project.history.insert_rear(task)
        return task

    # Complejidad: O(n)
    def process_rear(self, code: str) -> Task:
        project = self._project_service.require(code)
        if project.tasks.is_empty():
            raise EmptyDequeError("El proyecto no tiene tareas pendientes.")
        task = project.tasks.delete_rear()
        project.history.insert_rear(task)
        return task

    # Complejidad: O(n)
    def undo(self, code: str) -> Task:
        project = self._project_service.require(code)
        if project.history.is_empty():
            raise EmptyDequeError("El proyecto no tiene tareas procesadas para deshacer.")
        task = project.history.delete_rear()
        project.tasks.insert_front(task)
        return task
