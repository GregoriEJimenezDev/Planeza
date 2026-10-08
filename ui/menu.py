from __future__ import annotations

from config.settings import KIND_ERROR, KIND_WARN
from core.exceptions import EntityNotFoundError, PlanexaError
from factories.project_factory import ProjectFactory
from factories.task_factory import TaskFactory
from services.project_service import ProjectService
from services.report_service import ReportService
from services.system_status_service import SystemStatusService
from services.task_service import TaskService
from ui.commands.add_task_command import AddTaskCommand
from ui.commands.base_command import Command
from ui.commands.create_project_command import CreateProjectCommand
from ui.commands.delete_project_command import DeleteProjectCommand
from ui.commands.edit_project_command import EditProjectCommand
from ui.commands.exit_command import ExitCommand
from ui.commands.generate_report_command import GenerateReportCommand
from ui.commands.list_projects_command import ListProjectsCommand
from ui.commands.process_front_command import ProcessFrontCommand
from ui.commands.process_rear_command import ProcessRearCommand
from ui.commands.search_project_command import SearchProjectCommand
from ui.commands.system_status_command import SystemStatusCommand
from ui.commands.undo_command import UndoCommand
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class CommandFactory:
    """Construye la lista de comandos del menu (Open/Closed)."""

    # Complejidad: O(1)
    def __init__(
        self,
        project_service: ProjectService,
        task_service: TaskService,
        report_service: ReportService,
        status_service: SystemStatusService,
        project_factory: ProjectFactory,
        task_factory: TaskFactory,
    ) -> None:
        self._project_service = project_service
        self._task_service = task_service
        self._report_service = report_service
        self._status_service = status_service
        self._project_factory = project_factory
        self._task_factory = task_factory

    # Complejidad: O(n)
    def build(self) -> list[Command]:
        return [
            CreateProjectCommand(self._project_service, self._project_factory),
            SearchProjectCommand(self._project_service, self._project_factory),
            EditProjectCommand(self._project_service, self._project_factory),
            DeleteProjectCommand(self._project_service, self._project_factory),
            AddTaskCommand(self._task_service, self._task_factory, self._project_factory),
            ProcessFrontCommand(self._task_service, self._project_factory),
            ProcessRearCommand(self._task_service, self._project_factory),
            UndoCommand(self._task_service, self._project_factory),
            ListProjectsCommand(self._report_service),
            GenerateReportCommand(
                self._report_service, self._project_service, self._project_factory
            ),
            SystemStatusCommand(self._status_service),
            ExitCommand(self._status_service),
        ]


class Menu:
    # Complejidad: O(1)
    def __init__(
        self,
        commands: list[Command],
        renderer: Renderer,
        reader: Reader,
        summary_action,
    ) -> None:
        self._commands = commands
        self._renderer = renderer
        self._reader = reader
        self._summary_action = summary_action

    # Complejidad: O(n)
    def _render(self) -> None:
        self._renderer.clear()
        self._renderer.title("PLANEXA - Gestion de Proyectos y Tareas")
        lines = [
            self._renderer.center(f"{command.key}) {command.label}")
            for command in self._commands
        ]
        self._renderer.render_lines(lines)
        self._renderer.separator()

    # Complejidad: O(n)
    def _find(self, key: str) -> Command:
        for command in self._commands:
            if command.key == key:
                return command
        raise EntityNotFoundError(f"Opcion '{key}' no valida.")

    # Complejidad: O(n)
    def _shutdown(self) -> None:
        try:
            self._summary_action(self._renderer, self._reader)
        except (KeyboardInterrupt, EOFError):
            self._renderer.message(KIND_WARN, "Fallo al mostrar el resumen final.")

    # Complejidad: O(n)
    def run(self) -> None:
        options = [command.key for command in self._commands]
        running = True
        while running:
            self._render()
            try:
                choice = self._reader.read_choice("Seleccione una opcion", options)
                command = self._find(choice)
                running = command.execute(self._renderer, self._reader)
            except PlanexaError as error:
                self._renderer.message(KIND_ERROR, error.message)
                self._reader.wait_enter("Presione Enter para continuar...")
            except (KeyboardInterrupt, EOFError):
                self._renderer.message(KIND_WARN, "Sesion interrumpida por el usuario.")
                self._shutdown()
                return
        return
