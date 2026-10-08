from __future__ import annotations

from services.report_service import ReportService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class ListProjectsCommand(Command):
    # Complejidad: O(1)
    def __init__(self, report_service: ReportService) -> None:
        super().__init__("9", "Listar proyectos")
        self._report_service = report_service

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.title("Listar proyectos (front -> rear / rear -> front)")
        renderer.render_lines(self._report_service.generate_listing(False))
        renderer.render_lines(self._report_service.generate_listing(True))
        reader.wait_enter("Presione Enter para continuar...")
        return True
