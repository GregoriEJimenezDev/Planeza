"""Opcion 10: generar reportes A-F."""

from __future__ import annotations

from core.exceptions import EntityNotFoundError
from domain.project import Project
from factories.project_factory import ProjectFactory
from services.project_service import ProjectService
from services.report_service import ReportService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class GenerateReportCommand(Command):
    """Opcion 10: generar reportes A-F."""

    # Complejidad: O(1)
    def __init__(
        self,
        report_service: ReportService,
        project_service: ProjectService,
        project_factory: ProjectFactory,
    ) -> None:
        super().__init__("10", "Generar reportes (A-F)")
        self._report_service = report_service
        self._project_service = project_service
        self._project_factory = project_factory

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Generar Reporte")
        options = [
            "A) Inventario de proyectos (front -> rear)",
            "B) Inventario de proyectos (rear -> front)",
            "C) Tareas pendientes de un proyecto",
            "D) Historial de un proyecto",
            "E) Resumen de carga por proyecto",
            "F) Proyectos sin tareas pendientes",
        ]
        renderer.render_lines([renderer.center(option) for option in options])
        renderer.separator()
        identifier = reader.read_choice("Seleccione el reporte", ["A", "B", "C", "D", "E", "F"])
        project = self._resolve_project(identifier, reader)
        report = self._report_service.generate(identifier, project)
        renderer.clear()
        renderer.render_lines(report)
        reader.wait_enter("Presione Enter para continuar...")
        return True

    # Complejidad: O(n)
    def _resolve_project(self, identifier: str, reader: Reader) -> Project | None:
        if identifier not in ("C", "D"):
            return None
        code = reader.read_validated(
            "Codigo del proyecto", self._project_factory.code_validator
        )
        project = self._project_service.find_by_code(code)
        if project is None:
            raise EntityNotFoundError(f"No existe un proyecto con codigo '{code}'.")
        return project
