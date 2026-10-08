from __future__ import annotations

from config.settings import KIND_WARN
from core.exceptions import EntityNotFoundError
from services.project_service import ProjectService
from services.report_service import ReportService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class ListOrderCommand(Command):
    # Complejidad: O(1)
    def __init__(
        self,
        key: str,
        label: str,
        report_service: ReportService,
        reverse: bool,
    ) -> None:
        super().__init__(key, label)
        self._report_service = report_service
        self._reverse = reverse

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.render_lines(self._report_service.generate_listing(self._reverse))
        reader.wait_enter("Presione Enter para continuar...")
        return True


class BackCommand(Command):
    # Complejidad: O(1)
    def __init__(self) -> None:
        super().__init__("3", "Volver")

    # Complejidad: O(1)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        return False


class ListProjectsCommand(Command):
    # Complejidad: O(1)
    def __init__(
        self, report_service: ReportService, project_service: ProjectService
    ) -> None:
        super().__init__("9", "Listar proyectos")
        self._report_service = report_service
        self._project_service = project_service

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        if self._project_service.count() == 0:
            renderer.clear()
            renderer.message(KIND_WARN, "No hay proyectos registrados.")
            reader.wait_enter("Presione Enter para continuar...")
            return True
        options = [
            ListOrderCommand("1", "De front -> rear", self._report_service, False),
            ListOrderCommand("2", "De rear -> front", self._report_service, True),
            BackCommand(),
        ]
        running = True
        while running:
            renderer.clear()
            renderer.title("Listar proyectos")
            renderer.render_lines(
                [
                    renderer.center(f"{option.key}) {option.label}")
                    for option in options
                ]
            )
            renderer.separator()
            choice = reader.read_choice(
                "Seleccione el orden", [option.key for option in options]
            )
            running = self._find(options, choice).execute(renderer, reader)
        return True

    # Complejidad: O(n)
    def _find(self, options: list[Command], key: str) -> Command:
        for option in options:
            if option.key == key:
                return option
        raise EntityNotFoundError(f"Opcion '{key}' no valida.")
