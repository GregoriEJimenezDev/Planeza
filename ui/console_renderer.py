"""Renderer de consola centrado con ancho de contenido fijo."""

from __future__ import annotations

import os
import shutil
import sys
from abc import ABC, abstractmethod

from config.settings import CONTENT_WIDTH, MESSAGE_PREFIXES, TERMINAL_FALLBACK


class Renderer(ABC):
    """Interfaz de salida visual."""

    # Complejidad: O(1)
    @abstractmethod
    def clear(self) -> None:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def title(self, text: str) -> None:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def separator(self) -> None:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def message(self, kind: str, text: str) -> None:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def field(self, label: str, value: object) -> None:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def center(self, text: str) -> str:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def render_lines(self, lines: list[str]) -> None:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def prompt(self, label: str) -> None:
        ...


class ConsoleRenderer(Renderer):
    """Salida de consola centrada con ancho de contenido fijo."""

    # Complejidad: O(1)
    def __init__(self, content_width: int = CONTENT_WIDTH) -> None:
        self._content_width = content_width
        columns = shutil.get_terminal_size(fallback=TERMINAL_FALLBACK).columns
        self._margin = max(0, (columns - content_width) // 2)

    # Complejidad: O(1)
    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    # Complejidad: O(n)
    def _emit(self, line: str) -> None:
        sys.stdout.write(" " * self._margin + line + "\n")

    # Complejidad: O(n)
    def title(self, text: str) -> None:
        self._emit("=" * self._content_width)
        self._emit(text.center(self._content_width))
        self._emit("=" * self._content_width)

    # Complejidad: O(n)
    def separator(self) -> None:
        self._emit("-" * self._content_width)

    # Complejidad: O(n)
    def _wrap(self, text: str) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = word if not current else current + " " + word
            if len(candidate) <= self._content_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if not lines:
            lines.append("")
        return lines

    # Complejidad: O(n)
    def message(self, kind: str, text: str) -> None:
        prefix = MESSAGE_PREFIXES.get(kind, "")
        wrapped = self._wrap(text)
        first = True
        for line in wrapped:
            if first:
                rendered = f"{prefix} {line}".strip()
                first = False
            else:
                rendered = " " * (len(prefix) + 1) + line
            self._emit(rendered[: self._content_width])

    # Complejidad: O(n)
    def field(self, label: str, value: object) -> None:
        self._emit(f"{label}: {value}"[: self._content_width].ljust(self._content_width))

    # Complejidad: O(n)
    def center(self, text: str) -> str:
        return text.center(self._content_width)

    # Complejidad: O(n)
    def render_lines(self, lines: list[str]) -> None:
        for line in lines:
            self._emit(line)

    # Complejidad: O(n)
    def prompt(self, label: str) -> None:
        sys.stdout.write(" " * self._margin + label)
        sys.stdout.flush()
