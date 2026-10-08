from __future__ import annotations

from typing import TYPE_CHECKING

from core.exceptions import EntityNotFoundError
from domain.project import Project
from services.project_service import ProjectService

if TYPE_CHECKING:
    from builders.report_builder import AbstractReportBuilder, ReportBuilderFactory
    from builders.report_director import ReportSection


class ReportService:
    # Complejidad: O(1)
    def __init__(
        self,
        project_service: ProjectService,
        sections: list[ReportSection],
        builder_factory: ReportBuilderFactory,
    ) -> None:
        self._project_service = project_service
        self._sections = sections
        self._builder_factory = builder_factory

    # Complejidad: O(n)
    def _section(self, identifier: str) -> ReportSection | None:
        for section in self._sections:
            if section.identifier == identifier:
                return section
        return None

    # Complejidad: O(n)
    def generate(
        self, identifier: str, selected_project: Project | None = None
    ) -> list[str]:
        section = self._section(identifier)
        if section is None:
            raise EntityNotFoundError(f"No existe el reporte '{identifier}'.")
        builder = self._builder_factory.create()
        section.compose(builder, self._project_service, selected_project)
        return builder.build()

    # Complejidad: O(n)
    def generate_listing(self, reverse: bool) -> list[str]:
        builder = self._builder_factory.create()
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
        builder.total_records(count)
        return builder.build()
