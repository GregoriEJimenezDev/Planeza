"""Abstraccion Command de una opcion del menu."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ui.console_renderer import Renderer
from ui.input_reader import Reader


class Command(ABC):
    """Interfaz de una opcion del menu."""

    # Complejidad: O(1)
    def __init__(self, key: str, label: str) -> None:
        self.key = key
        self.label = label

    # Complejidad: O(n)
    @abstractmethod
    def execute(self, renderer: Renderer, reader: Reader) -> bool:
        ...
