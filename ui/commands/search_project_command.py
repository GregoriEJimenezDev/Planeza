"""Opcion 2: buscar proyecto."""

from __future__ import annotations

from factories.project_factory import ProjectFactory
from services.project_service import ProjectService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class SearchProjectCommand(Command):
    """Opcion 2: buscar proyecto."""

    # Complejidad: O(1)
    def __init__(self, project_service: ProjectService, factory: ProjectFactory) -> None:
        super().__init__("2", "Buscar proyecto")
        self._project_service = project_service
        self._factory = factory

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Buscar Proyecto")
        code = reader.read_validated("Codigo del proyecto", self._factory.code_validator)
        project = self._project_service.require(code)
        renderer.separator()
        renderer.field("Codigo", project.code)
        renderer.field("Nombre", project.name)
        renderer.field("Descripcion", project.description)
        renderer.field("Fecha de inicio", project.start_date.isoformat())
        renderer.field("Tareas pendientes", project.pending_count)
        renderer.field("Tareas procesadas", project.processed_count)
        renderer.separator()
        reader.wait_enter("Presione Enter para continuar...")
        return True
