from __future__ import annotations

from typing import TYPE_CHECKING

from services.project_service import ProjectService

if TYPE_CHECKING:
    from builders.report_builder import ReportBuilderFactory


class SystemStatusService:
    # Complejidad: O(1)
    def __init__(
        self, project_service: ProjectService, builder_factory: ReportBuilderFactory
    ) -> None:
        self._project_service = project_service
        self._builder_factory = builder_factory

    # Complejidad: O(1)
    def _label(self, project) -> str:
        if project is None:
            return "(no hay)"
        return f"{project.code} - {project.name}"

    # Complejidad: O(1)
    def _most_label(self, project) -> str:
        if project is None:
            return "(no hay)"
        return f"{project.code} - {project.name} ({project.tasks.size})"

    # Complejidad: O(n)
    def status_pairs(self) -> list[tuple[str, object]]:
        first = self._project_service.first_project()
        last = self._project_service.last_project()
        most = self._project_service.most_tasks_project()
        return [
            ("Total de proyectos", self._project_service.count()),
            ("Primer proyecto", self._label(first)),
            ("Ultimo proyecto", self._label(last)),
            ("Tareas activas", self._project_service.total_pending_tasks()),
            ("Proyecto con más tareas", self._most_label(most)),
            ("Tareas procesadas", self._project_service.total_processed_tasks()),
        ]

    # Complejidad: O(n)
    def summary_pairs(self) -> list[tuple[str, object]]:
        return [
            ("Total de proyectos", self._project_service.count()),
            ("Tareas activas", self._project_service.total_pending_tasks()),
            ("Tareas procesadas", self._project_service.total_processed_tasks()),
        ]

    # Complejidad: O(n)
    def status_report(self) -> list[str]:
        builder = self._builder_factory.create()
        builder.header("Estado del sistema", "S")
        pairs = self.status_pairs()
        for label, value in pairs:
            builder.pair(label, value)
        builder.total_records(len(pairs))
        return builder.build()

    # Complejidad: O(n)
    def summary_report(self) -> list[str]:
        builder = self._builder_factory.create()
        builder.header("Resumen final de la sesión", "R")
        pairs = self.summary_pairs()
        for label, value in pairs:
            builder.pair(label, value)
        builder.total_records(len(pairs))
        builder.footer("Fin de la sesión - Planexa")
        return builder.build()
