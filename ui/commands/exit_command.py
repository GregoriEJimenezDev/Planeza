"""Opcion 12: salir con confirmacion y resumen final."""

from __future__ import annotations

from config.settings import KIND_INFO
from services.report_service import ReportService
from services.system_status_service import SystemStatusService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class ExitCommand(Command):
    """Opcion 12: salir con confirmacion y resumen final."""

    # Complejidad: O(1)
    def __init__(
        self, report_service: ReportService, status_service: SystemStatusService
    ) -> None:
        super().__init__("12", "Salir")
        self._report_service = report_service
        self._status_service = status_service

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        if not reader.read_yes_no("Desea salir del sistema"):
            renderer.message(KIND_INFO, "Salida cancelada.")
            reader.wait_enter("Presione Enter para continuar...")
            return True
        pairs = self._status_service.summary_pairs()
        renderer.clear()
        renderer.render_lines(self._report_service.generate_summary(pairs))
        reader.wait_enter("Presione Enter para salir...")
        return False
