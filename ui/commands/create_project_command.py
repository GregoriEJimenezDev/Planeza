"""Opcion 1: crear proyecto."""

from __future__ import annotations

from config.settings import KIND_OK
from factories.project_factory import ProjectFactory
from services.project_service import ProjectService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class CreateProjectCommand(Command):
    """Opcion 1: crear proyecto."""

    # Complejidad: O(1)
    def __init__(self, project_service: ProjectService, factory: ProjectFactory) -> None:
        super().__init__("1", "Crear proyecto")
        self._project_service = project_service
        self._factory = factory

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Crear Proyecto")
        code = reader.read_validated("Codigo del proyecto", self._factory.code_validator)
        name = reader.read_validated("Nombre", self._factory.name_validator)
        description = reader.read_validated("Descripcion", self._factory.description_validator)
        start_date = reader.read_date("Fecha de inicio (DD-MM-AAAA)")
        project = self._project_service.create(code, name, description, start_date)
        renderer.message(KIND_OK, f"Proyecto '{project.code}' creado correctamente.")
        reader.wait_enter("Presione Enter para continuar...")
        return True
