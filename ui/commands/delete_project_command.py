from __future__ import annotations

from config.settings import KIND_OK
from factories.project_factory import ProjectFactory
from services.project_service import ProjectService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class DeleteProjectCommand(Command):
    # Complejidad: O(1)
    def __init__(self, project_service: ProjectService, factory: ProjectFactory) -> None:
        super().__init__("4", "Eliminar proyecto")
        self._project_service = project_service
        self._factory = factory

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Eliminar proyecto")
        code = reader.read_validated("Codigo del proyecto", self._factory.code_validator)
        project = self._project_service.delete(code)
        renderer.message(KIND_OK, f"Proyecto '{project.code}' eliminado correctamente.")
        reader.wait_enter("Presione Enter para continuar...")
        return True
