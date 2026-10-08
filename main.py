"""PLANEXA - Practica 2.

Punto unico de composicion: arma las dependencias y arranca el menu.
Arquitectura por capas: ui -> services -> domain -> core.
"""

from __future__ import annotations

from builders.report_builder import ReportBuilderFactory
from builders.report_director import (
    SectionA,
    SectionB,
    SectionC,
    SectionD,
    SectionE,
    SectionF,
)
from config.settings import CONTENT_WIDTH, DATE_FORMAT
from core.deque import Deque
from factories import DateValidator, NotEmptyValidator, PositiveNumberValidator
from factories.project_factory import ProjectFactory
from factories.task_factory import TaskFactory
from services.project_service import ProjectService
from services.report_service import ReportService
from services.system_status_service import SystemStatusService
from services.task_service import TaskService
from ui.console_renderer import ConsoleRenderer, Renderer
from ui.input_reader import ConsoleInputReader, Reader
from ui.menu import CommandFactory, Menu


# Complejidad: O(1)
def build_summary_action(status_service: SystemStatusService):
    # Complejidad: O(n)
    def action(renderer: Renderer, reader: Reader) -> None:
        renderer.clear()
        renderer.render_lines(status_service.summary_report())
        reader.wait_enter("Presione Enter para salir...")

    return action


# Complejidad: O(1)
def build_application() -> Menu:
    renderer = ConsoleRenderer(CONTENT_WIDTH)
    reader = ConsoleInputReader(renderer)

    code_validator = NotEmptyValidator("codigo")
    name_validator = NotEmptyValidator("nombre")
    description_validator = NotEmptyValidator("descripcion")
    responsible_validator = NotEmptyValidator("responsable")
    date_validator = DateValidator("fecha", DATE_FORMAT)
    task_id_validator = NotEmptyValidator("id de tarea")
    title_validator = NotEmptyValidator("titulo")
    priority_validator = NotEmptyValidator("prioridad")
    estimation_validator = PositiveNumberValidator("estimacion")

    project_factory = ProjectFactory(
        code_validator,
        name_validator,
        description_validator,
        responsible_validator,
        date_validator,
    )
    task_factory = TaskFactory(
        task_id_validator,
        title_validator,
        description_validator,
        priority_validator,
        estimation_validator,
    )

    projects = Deque()
    project_service = ProjectService(projects, project_factory)
    task_service = TaskService(project_service, task_factory)
    builder_factory = ReportBuilderFactory(CONTENT_WIDTH)
    status_service = SystemStatusService(project_service, builder_factory)

    sections = [
        SectionA(),
        SectionB(),
        SectionC(),
        SectionD(),
        SectionE(),
        SectionF(),
    ]
    report_service = ReportService(project_service, sections, builder_factory)

    command_factory = CommandFactory(
        project_service,
        task_service,
        report_service,
        status_service,
        project_factory,
        task_factory,
    )
    commands = command_factory.build()
    summary_action = build_summary_action(status_service)
    return Menu(commands, renderer, reader, summary_action)


# Complejidad: O(n)
def main() -> None:
    menu = build_application()
    menu.run()


if __name__ == "__main__":
    main()
