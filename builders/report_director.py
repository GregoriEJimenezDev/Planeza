from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.exceptions import ValidationError
from domain.project import Project

if TYPE_CHECKING:
    from builders.report_builder import AbstractReportBuilder
    from services.project_service import ProjectService


TASK_COLUMNS = [
    ("ID", 10, "left"),
    ("TITULO", 28, "left"),
    ("PRIORIDAD", 12, "left"),
    ("HORAS", 8, "right"),
]


class ReportSection(ABC):
    # Complejidad: O(1)
    def __init__(self, identifier: str, title: str) -> None:
        self.identifier = identifier
        self.title = title

    # Complejidad: O(n)
    @abstractmethod
    def compose(
        self,
        builder: AbstractReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        ...


class SectionA(ReportSection):
    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("A", "Total de proyectos registrados")

    # Complejidad: O(n)
    def compose(
        self,
        builder: AbstractReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        builder.header(self.title, self.identifier)
        count = 0
        for _ in project_service.iter_projects(False):
            count += 1
        builder.pair("Total de proyectos registrados", count)
        builder.total_records(1)


class SectionB(ReportSection):
    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("B", "Tareas de un proyecto (front -> rear)")

    # Complejidad: O(n)
    def compose(
        self,
        builder: AbstractReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        if selected_project is None:
            raise ValidationError("El reporte B requiere un proyecto.")
        builder.header(self.title, self.identifier)
        builder.metadata("Proyecto", f"{selected_project.code} - {selected_project.name}")
        builder.metadata("Orden", "front -> rear")
        builder.table(TASK_COLUMNS)
        count = 0
        for task in selected_project.tasks:
            builder.row(
                [task.task_id, task.title, task.priority, f"{task.estimation:g}"]
            )
            count += 1
        builder.total_records(count)


class SectionC(ReportSection):
    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("C", "Tareas de un proyecto (rear -> front)")

    # Complejidad: O(n)
    def compose(
        self,
        builder: AbstractReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        if selected_project is None:
            raise ValidationError("El reporte C requiere un proyecto.")
        builder.header(self.title, self.identifier)
        builder.metadata("Proyecto", f"{selected_project.code} - {selected_project.name}")
        builder.metadata("Orden", "rear -> front")
        builder.table(TASK_COLUMNS)
        count = 0
        for task in selected_project.tasks.iter_reverse():
            builder.row(
                [task.task_id, task.title, task.priority, f"{task.estimation:g}"]
            )
            count += 1
        builder.total_records(count)


class SectionD(ReportSection):
    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("D", "Proyecto con más tareas")

    # Complejidad: O(n)
    def compose(
        self,
        builder: AbstractReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        builder.header(self.title, self.identifier)
        most = project_service.most_tasks_project()
        if most is None:
            builder.note("Sin registros")
            builder.total_records(0)
            return
        builder.pair(
            "Proyecto con más tareas",
            f"{most.code} - {most.name} ({most.tasks.size})",
        )
        builder.total_records(1)


class SectionE(ReportSection):
    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("E", "Total de tareas de todos los proyectos")

    # Complejidad: O(n)
    def compose(
        self,
        builder: AbstractReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        builder.header(self.title, self.identifier)
        total = project_service.total_pending_tasks()
        builder.pair("Total de tareas de todos los proyectos", total)
        builder.total_records(1)


class SectionF(ReportSection):
    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("F", "Historial de tareas procesadas de un proyecto")

    # Complejidad: O(n)
    def compose(
        self,
        builder: AbstractReportBuilder,
        project_service: ProjectService,
        selected_project: Project | None,
    ) -> None:
        if selected_project is None:
            raise ValidationError("El reporte F requiere un proyecto.")
        builder.header(self.title, self.identifier)
        builder.metadata("Proyecto", f"{selected_project.code} - {selected_project.name}")
        builder.metadata("Orden", "front -> rear")
        builder.table(TASK_COLUMNS)
        count = 0
        for task in selected_project.history:
            builder.row(
                [task.task_id, task.title, task.priority, f"{task.estimation:g}"]
            )
            count += 1
        builder.total_records(count)
