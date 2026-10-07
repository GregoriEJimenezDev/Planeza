"""Director de reportes: arma cada seccion A-F usando el ReportBuilder."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from builders.report_builder import ReportBuilder
from core.exceptions import ValidationError
from domain.project import Project

if TYPE_CHECKING:
    from services.project_service import ProjectService


class ReportSection(ABC):
    """Estrategia de composicion de una seccion de reporte."""

    # Complejidad: O(1)
    def __init__(self, identifier: str, title: str) -> None:
        self.identifier = identifier
        self.title = title

    # Complejidad: O(n)
    @abstractmethod
    def compose(
        self,
        builder: ReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        ...


class SectionA(ReportSection):
    """Inventario de proyectos front -> rear."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("A", "Inventario de proyectos")

    # Complejidad: O(n)
    def compose(
        self,
        builder: ReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        builder.header(self.title, self.identifier)
        builder.metadata("Orden", "front -> rear")
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
        for project in project_service.iter_projects(False):
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


class SectionB(ReportSection):
    """Inventario de proyectos rear -> front."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("B", "Inventario de proyectos (inverso)")

    # Complejidad: O(n)
    def compose(
        self,
        builder: ReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        builder.header(self.title, self.identifier)
        builder.metadata("Orden", "rear -> front")
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
        for project in project_service.iter_projects(True):
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


class SectionC(ReportSection):
    """Tareas pendientes de un proyecto front -> rear."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("C", "Tareas pendientes")

    # Complejidad: O(n)
    def compose(
        self,
        builder: ReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        if selected_project is None:
            raise ValidationError("El reporte C requiere un proyecto.")
        builder.header(self.title, self.identifier)
        builder.metadata("Proyecto", f"{selected_project.code} - {selected_project.name}")
        builder.metadata("Orden", "front -> rear")
        builder.table(
            [
                ("ID", 10, "left"),
                ("TITULO", 30, "left"),
                ("HORAS", 8, "right"),
                ("VENCE", 12, "left"),
            ]
        )
        count = 0
        for task in selected_project.tasks:
            builder.row(
                [
                    task.task_id,
                    task.title,
                    f"{task.estimation:g}",
                    task.due_date.isoformat(),
                ]
            )
            count += 1
        builder.totals(f"Total de registros: {count}")


class SectionD(ReportSection):
    """Historial de un proyecto rear -> front."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("D", "Historial de tareas")

    # Complejidad: O(n)
    def compose(
        self,
        builder: ReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        if selected_project is None:
            raise ValidationError("El reporte D requiere un proyecto.")
        builder.header(self.title, self.identifier)
        builder.metadata("Proyecto", f"{selected_project.code} - {selected_project.name}")
        builder.metadata("Orden", "rear -> front")
        builder.table(
            [
                ("ID", 10, "left"),
                ("TITULO", 30, "left"),
                ("HORAS", 8, "right"),
                ("VENCE", 12, "left"),
            ]
        )
        count = 0
        for task in selected_project.history.iter_reverse():
            builder.row(
                [
                    task.task_id,
                    task.title,
                    f"{task.estimation:g}",
                    task.due_date.isoformat(),
                ]
            )
            count += 1
        builder.totals(f"Total de registros: {count}")


class SectionE(ReportSection):
    """Resumen de carga por proyecto."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("E", "Resumen de carga por proyecto")

    # Complejidad: O(n)
    def compose(
        self,
        builder: ReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        builder.header(self.title, self.identifier)
        builder.metadata("Orden", "front -> rear")
        builder.table(
            [
                ("CODIGO", 10, "left"),
                ("NOMBRE", 22, "left"),
                ("PEND", 7, "right"),
                ("PROC", 7, "right"),
                ("HORAS", 8, "right"),
            ]
        )
        count = 0
        for project in project_service.iter_projects(False):
            pending_hours = 0.0
            for task in project.tasks:
                pending_hours += task.estimation
            builder.row(
                [
                    project.code,
                    project.name,
                    project.pending_count,
                    project.processed_count,
                    f"{pending_hours:g}",
                ]
            )
            count += 1
        builder.totals(f"Total de registros: {count}")


class SectionF(ReportSection):
    """Proyectos sin tareas pendientes."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("F", "Proyectos sin tareas pendientes")

    # Complejidad: O(n)
    def compose(
        self,
        builder: ReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        builder.header(self.title, self.identifier)
        builder.metadata("Orden", "front -> rear")
        builder.table(
            [
                ("CODIGO", 10, "left"),
                ("NOMBRE", 30, "left"),
                ("PROC", 7, "right"),
            ]
        )
        count = 0
        for project in project_service.iter_projects(False):
            if project.tasks.is_empty():
                builder.row(
                    [project.code, project.name, project.processed_count]
                )
                count += 1
        builder.totals(f"Total de registros: {count}")
