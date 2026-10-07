"""Servicio de estado del sistema y resumen final."""

from __future__ import annotations

from services.project_service import ProjectService


class SystemStatusService:
    """Calcula metricas globales recorriendo el Deque real."""

    # Complejidad: O(1)
    def __init__(self, project_service: ProjectService) -> None:
        self._project_service = project_service

    # Complejidad: O(n)
    def _totals(self) -> tuple[int, int, int, float]:
        total_projects = 0
        pending = 0
        processed = 0
        pending_estimation = 0.0
        for project in self._project_service.iter_projects():
            total_projects += 1
            pending += project.tasks.size
            processed += project.history.size
            for task in project.tasks:
                pending_estimation += task.estimation
        return total_projects, pending, processed, pending_estimation

    # Complejidad: O(n)
    def status_pairs(self) -> list[tuple[str, object]]:
        total_projects, pending, processed, pending_estimation = self._totals()
        return [
            ("Proyectos registrados", total_projects),
            ("Tareas pendientes", pending),
            ("Tareas procesadas", processed),
            ("Horas pendientes", f"{pending_estimation:g}"),
        ]

    # Complejidad: O(n)
    def summary_pairs(self) -> list[tuple[str, object]]:
        total_projects, pending, processed, _ = self._totals()
        return [
            ("Total de proyectos", total_projects),
            ("Tareas pendientes", pending),
            ("Tareas procesadas", processed),
        ]
