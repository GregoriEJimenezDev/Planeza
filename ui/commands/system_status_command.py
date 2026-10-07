"""Opcion 11: ver estado del sistema."""

from __future__ import annotations

from services.report_service import ReportService
from services.system_status_service import SystemStatusService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class SystemStatusCommand(Command):
    """Opcion 11: ver estado del sistema."""

    # Complejidad: O(1)
    def __init__(
        self, report_service: ReportService, status_service: SystemStatusService
    ) -> None:
        super().__init__("11", "Ver estado del sistema")
        self._report_service = report_service
        self._status_service = status_service

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        pairs = self._status_service.status_pairs()
        renderer.render_lines(self._report_service.generate_status(pairs))
        reader.wait_enter("Presione Enter para continuar...")
        return True
