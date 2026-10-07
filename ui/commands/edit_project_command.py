"""Opcion 3: editar proyecto (el codigo no se edita)."""

from __future__ import annotations

from config.settings import KIND_OK
from factories.project_factory import ProjectFactory
from services.project_service import ProjectService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class EditProjectCommand(Command):
    """Opcion 3: editar proyecto (el codigo no se edita)."""

    # Complejidad: O(1)
    def __init__(self, project_service: ProjectService, factory: ProjectFactory) -> None:
        super().__init__("3", "Editar proyecto")
        self._project_service = project_service
        self._factory = factory

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Editar Proyecto")
        code = reader.read_validated("Codigo del proyecto", self._factory.code_validator)
        project = self._project_service.require(code)
        name = reader.read_validated("Nuevo nombre", self._factory.name_validator)
        description = reader.read_validated(
            "Nueva descripcion", self._factory.description_validator
        )
        self._project_service.update(code, name, description)
        renderer.message(KIND_OK, f"Proyecto '{project.code}' actualizado correctamente.")
        reader.wait_enter("Presione Enter para continuar...")
        return True
