from __future__ import annotations

from core.deque import Deque
from factories.project_factory import ProjectFactory
from services.project_service import ProjectService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class SearchProjectCommand(Command):
    # Complejidad: O(1)
    def __init__(self, project_service: ProjectService, factory: ProjectFactory) -> None:
        super().__init__("2", "Buscar proyecto")
        self._project_service = project_service
        self._factory = factory

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Buscar proyecto")
        code = reader.read_validated("Codigo del proyecto", self._factory.code_validator)
        project = self._project_service.require(code)
        renderer.separator()
        renderer.field("Codigo", project.code)
        renderer.field("Nombre", project.name)
        renderer.field("Descripcion", project.description)
        renderer.field("Responsable", project.responsible)
        renderer.field("Fecha de inicio", project.start_date.isoformat())
        renderer.field("Cantidad de tareas", project.pending_count)
        renderer.field("Primera tarea pendiente", self._task_label(project.tasks, True))
        renderer.field("Ultima tarea pendiente", self._task_label(project.tasks, False))
        renderer.field("Ultima tarea procesada", self._task_label(project.history, False))
        renderer.field("Tareas procesadas", project.processed_count)
        renderer.separator()
        reader.wait_enter("Presione Enter para continuar...")
        return True

    # Complejidad: O(1)
    def _task_label(self, tasks: Deque, use_front: bool) -> str:
        if tasks.is_empty():
            return "Sin tareas"
        task = tasks.get_front() if use_front else tasks.get_rear()
        return f"{task.task_id} - {task.title}"
