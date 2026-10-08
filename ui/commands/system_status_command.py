from __future__ import annotations

from services.system_status_service import SystemStatusService
from ui.commands.base_command import Command
from ui.console_renderer import Renderer
from ui.input_reader import Reader


class SystemStatusCommand(Command):
    # Complejidad: O(1)
    def __init__(self, status_service: SystemStatusService) -> None:
        super().__init__("11", "Ver estado del sistema")
        self._status_service = status_service

    # Complejidad: O(n)
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        renderer.clear()
        renderer.render_lines(self._status_service.status_report())
        reader.wait_enter("Presione Enter para continuar...")
        return True
