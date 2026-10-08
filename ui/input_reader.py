from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from datetime import datetime

try:
    import msvcrt
except ImportError:
    msvcrt = None

from config.settings import KIND_ERROR, KIND_WARN
from core.exceptions import ValidationError
from factories import Validator
from ui.console_renderer import Renderer


class Reader(ABC):
    # Complejidad: O(n)
    @abstractmethod
    def read_validated(self, label: str, validator: Validator) -> object:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def read_choice(self, label: str, options: list[str]) -> str:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def read_yes_no(self, label: str) -> bool:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def read_date(self, label: str) -> str:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def wait_enter(self, label: str) -> None:
        ...


class ConsoleInputReader(Reader):
    # Complejidad: O(1)
    def __init__(self, renderer: Renderer) -> None:
        self._renderer = renderer

    # Complejidad: O(n)
    def _read_raw(self, label: str) -> str:
        self._renderer.prompt(label)
        return input().strip()

    # Complejidad: O(n)
    def read_validated(self, label: str, validator: Validator) -> object:
        while True:
            raw = self._read_raw(f"{label}: ")
            try:
                return validator.validate(raw)
            except ValidationError as error:
                self._renderer.message(KIND_ERROR, error.message)

    # Complejidad: O(n)
    def read_choice(self, label: str, options: list[str]) -> str:
        while True:
            raw = self._read_raw(f"{label}: ").upper()
            if raw in options:
                return raw
            self._renderer.message(KIND_WARN, "Opcion invalida. Intente nuevamente.")

    # Complejidad: O(n)
    def read_yes_no(self, label: str) -> bool:
        while True:
            raw = self._read_raw(f"{label} (s/n): ").lower()
            if raw in ("s", "n"):
                return raw == "s"
            self._renderer.message(KIND_WARN, "Responda 's' o 'n'.")

    # Complejidad: O(n)
    def _format_date_mask(self, digits: str) -> str:
        text = digits[0:2]
        if len(digits) >= 2:
            text += "-" + digits[2:4]
            if len(digits) >= 4:
                text += "-" + digits[4:8]
        return text

    # Complejidad: O(n)
    def _read_date_plain(self, label: str) -> str:
        self._renderer.prompt(f"{label}: ")
        return input().strip()

    # Complejidad: O(n)
    def _read_date_mask(self, label: str) -> str:
        if msvcrt is None or not sys.stdin.isatty():
            return self._read_date_plain(label)
        self._renderer.prompt(f"{label}: ")
        digits = ""
        printed = ""
        while True:
            key = msvcrt.getwch()
            if key in ("\x00", "\xe0"):
                msvcrt.getwch()
                continue
            if key == "\r":
                sys.stdout.write("\n")
                sys.stdout.flush()
                return digits
            if key == "\x03":
                raise KeyboardInterrupt
            if key == "\x1a":
                raise EOFError
            if key in ("\x08", "\x7f"):
                digits = digits[:-1]
            elif key.isdigit() and len(digits) < 8:
                digits += key
            else:
                continue
            rendered = self._format_date_mask(digits)
            sys.stdout.write(
                "\b" * len(printed) + " " * len(printed) + "\b" * len(printed) + rendered
            )
            sys.stdout.flush()
            printed = rendered

    # Complejidad: O(n)
    def read_date(self, label: str) -> str:
        while True:
            raw = self._read_date_mask(label).strip()
            for date_format in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y"):
                try:
                    return datetime.strptime(raw, date_format).date().isoformat()
                except ValueError:
                    continue
            digits = "".join(character for character in raw if character.isdigit())
            if len(digits) == 8:
                packed = f"{digits[0:2]}-{digits[2:4]}-{digits[4:8]}"
                try:
                    return datetime.strptime(packed, "%d-%m-%Y").date().isoformat()
                except ValueError:
                    pass
            self._renderer.message(
                KIND_ERROR, "Fecha invalida. Use DD-MM-AAAA (ej. 02-06-2005)."
            )

    # Complejidad: O(n)
    def wait_enter(self, label: str) -> None:
        self._renderer.prompt(label)
        input()
