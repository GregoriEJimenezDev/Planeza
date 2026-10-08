from __future__ import annotations

from config.settings import KIND_OK
from factories.project_factory import ProjectFactory
from services.task_service import TaskService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class ProcessFrontCommand(Command):
    # Complejidad: O(1)
    def __init__(self, task_service: TaskService, project_factory: ProjectFactory) -> None:
        super().__init__("6", "Procesar tarea por el frente")
        self._task_service = task_service
        self._project_factory = project_factory

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Procesar tarea por el frente")
        code = reader.read_validated(
            "Codigo del proyecto", self._project_factory.code_validator
        )
        task = self._task_service.process_front(code)
        renderer.message(KIND_OK, f"Tarea procesada: {task.task_id} - {task.title}")
        reader.wait_enter("Presione Enter para continuar...")
        return True
