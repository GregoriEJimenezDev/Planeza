"""Servicio de reportes: orquesta la construccion con plantilla unica."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from builders.report_builder import ReportBuilder
from config.settings import CONTENT_WIDTH, DATETIME_FORMAT
from core.exceptions import EntityNotFoundError
from domain.project import Project
from services.project_service import ProjectService

if TYPE_CHECKING:
    from builders.report_director import ReportSection


class ReportService:
    """Orquesta la construccion de todos los reportes con plantilla unica."""

    # Complejidad: O(n)
    def __init__(self, project_service: ProjectService, sections: list[ReportSection]) -> None:
        self._project_service = project_service
        self._sections = sections

    # Complejidad: O(1)
    def _new_builder(self) -> ReportBuilder:
        builder = ReportBuilder(CONTENT_WIDTH)
        builder.metadata("Generado", datetime.now().strftime(DATETIME_FORMAT))
        return builder

    # Complejidad: O(n)
    def _section(self, identifier: str) -> ReportSection | None:
        for section in self._sections:
            if section.identifier == identifier:
                return section
        return None

    # Complejidad: O(n)
    def generate(self, identifier: str, selected_project: Project | None = None) -> list[str]:
        section = self._section(identifier)
        if section is None:
            raise EntityNotFoundError(f"No existe el reporte '{identifier}'.")
        builder = self._new_builder()
        section.compose(builder, self._project_service, selected_project)
        return builder.build()

    # Complejidad: O(n)
    def generate_listing(self, reverse: bool) -> list[str]:
        builder = self._new_builder()
        builder.header("Listado de proyectos", "L")
        builder.metadata("Orden", "rear -> front" if reverse else "front -> rear")
        builder.table(
            [
                ("CODIGO", 10, "left"),
                ("NOMBRE", 26, "left"),
                ("INICIO", 12, "left"),
                ("PEND", 7, "right"),
                ("PROC", 7, "right"),
            ]
        )
        count = 0
        for project in self._project_service.iter_projects(reverse):
            builder.row(
                [
                    project.code,
                    project.name,
                    project.start_date.isoformat(),
                    project.pending_count,
                    project.processed_count,
                ]
            )
            count += 1
        builder.totals(f"Total de registros: {count}")
        return builder.build()

    # Complejidad: O(n)
    def generate_status(self, pairs: list[tuple[str, object]]) -> list[str]:
        builder = self._new_builder()
        builder.header("Estado del sistema", "S")
        for label, value in pairs:
            builder.pair(label, value)
        builder.totals(f"Total de registros: {len(pairs)}")
        return builder.build()

    # Complejidad: O(n)
    def generate_summary(self, pairs: list[tuple[str, object]]) -> list[str]:
        builder = self._new_builder()
        builder.header("Resumen final de la sesion", "R")
        for label, value in pairs:
            builder.pair(label, value)
        builder.totals(f"Total de registros: {len(pairs)}")
        builder.footer("Fin de la sesion - Planexa")
        return builder.build()
