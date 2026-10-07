"""Opcion 5: anadir tarea a un proyecto."""

from __future__ import annotations

from config.settings import KIND_OK
from factories.project_factory import ProjectFactory
from factories.task_factory import TaskFactory
from services.task_service import TaskService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class AddTaskCommand(Command):
    """Opcion 5: anadir tarea a un proyecto."""

    # Complejidad: O(1)
    def __init__(
        self,
        task_service: TaskService,
        factory: TaskFactory,
        project_factory: ProjectFactory,
    ) -> None:
        super().__init__("5", "Anadir tarea")
        self._task_service = task_service
        self._factory = factory
        self._project_factory = project_factory

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Anadir Tarea")
        code = reader.read_validated(
            "Codigo del proyecto", self._project_factory.code_validator
        )
        task_id = reader.read_validated("ID de la tarea", self._factory.id_validator)
        title = reader.read_validated("Titulo", self._factory.title_validator)
        description = reader.read_validated(
            "Descripcion", self._factory.description_validator
        )
        estimation = reader.read_validated(
            "Estimacion en horas", self._factory.estimation_validator
        )
        due_date = reader.read_date("Fecha de vencimiento (DD-MM-AAAA)")
        task = self._task_service.add_task(
            code, task_id, title, description, estimation, due_date
        )
        renderer.message(KIND_OK, f"Tarea '{task.task_id}' anadida al proyecto '{code}'.")
        reader.wait_enter("Presione Enter para continuar...")
        return True
