from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from config.settings import (
    CONTENT_WIDTH,
    DATETIME_FORMAT,
    EMPTY_RECORDS,
    FOOTER_TEXT,
    SYSTEM_NAME,
    TOTALS_LABEL,
)


class AbstractReportBuilder(ABC):
    # Complejidad: O(1)
    @abstractmethod
    def header(self, title: str, identifier: str) -> AbstractReportBuilder:
        ...

    # Complejidad: O(1)
    @abstractmethod
    def metadata(self, label: str, value: object) -> AbstractReportBuilder:
        ...

    # Complejidad: O(1)
    @abstractmethod
    def table(self, columns: list[tuple[str, int, str]]) -> AbstractReportBuilder:
        ...

    # Complejidad: O(1)
    @abstractmethod
    def row(self, values: list[object]) -> AbstractReportBuilder:
        ...

    # Complejidad: O(1)
    @abstractmethod
    def pair(self, label: str, value: object) -> AbstractReportBuilder:
        ...

    # Complejidad: O(1)
    @abstractmethod
    def note(self, text: str) -> AbstractReportBuilder:
        ...

    # Complejidad: O(1)
    @abstractmethod
    def total_records(self, count: int) -> AbstractReportBuilder:
        ...

    # Complejidad: O(1)
    @abstractmethod
    def footer(self, text: str) -> AbstractReportBuilder:
        ...

    # Complejidad: O(n)
    @abstractmethod
    def build(self) -> list[str]:
        ...


class ReportBuilder(AbstractReportBuilder):
    # Complejidad: O(1)
    def __init__(self, width: int = CONTENT_WIDTH) -> None:
        self._width = width
        self._title = ""
        self._identifier = ""
        self._metadata: list[tuple[str, str]] = []
        self._columns: list[tuple[str, int, str]] = []
        self._rows: list[list[object]] = []
        self._pairs: list[tuple[str, object]] = []
        self._note = EMPTY_RECORDS
        self._totals = ""
        self._footer = FOOTER_TEXT

    # Complejidad: O(1)
    def header(self, title: str, identifier: str) -> ReportBuilder:
        self._title = title
        self._identifier = identifier
        return self

    # Complejidad: O(1)
    def metadata(self, label: str, value: object) -> ReportBuilder:
        self._metadata.append((label, str(value)))
        return self

    # Complejidad: O(1)
    def table(self, columns: list[tuple[str, int, str]]) -> ReportBuilder:
        self._columns = columns
        return self

    # Complejidad: O(1)
    def row(self, values: list[object]) -> ReportBuilder:
        self._rows.append(values)
        return self

    # Complejidad: O(1)
    def pair(self, label: str, value: object) -> ReportBuilder:
        self._pairs.append((label, value))
        return self

    # Complejidad: O(1)
    def note(self, text: str) -> ReportBuilder:
        self._note = text
        return self

    # Complejidad: O(1)
    def total_records(self, count: int) -> ReportBuilder:
        self._totals = f"{TOTALS_LABEL}: {count}"
        return self

    # Complejidad: O(1)
    def footer(self, text: str) -> ReportBuilder:
        self._footer = text
        return self

    # Complejidad: O(n)
    def _center(self, text: str) -> str:
        return text.center(self._width)

    # Complejidad: O(n)
    def _format_row(self, values: list[object], columns: list[tuple[str, int, str]]) -> str:
        cells: list[str] = []
        for value, (_, width, align) in zip(values, columns):
            text = str(value)
            if len(text) > width:
                text = text[:width]
            if align == "right":
                cells.append(text.rjust(width))
            elif align == "center":
                cells.append(text.center(width))
            else:
                cells.append(text.ljust(width))
        return (" " + " ".join(cells)).ljust(self._width)

    # Complejidad: O(n)
    def build(self) -> list[str]:
        lines: list[str] = []
        lines.append("=" * self._width)
        lines.append(self._center(SYSTEM_NAME.upper()))
        lines.append(self._center(f"Reporte {self._identifier} - {self._title}"))
        lines.append("=" * self._width)
        for label, value in self._metadata:
            lines.append(f" {label}: {value}".ljust(self._width))
        lines.append("-" * self._width)
        if self._columns:
            effective = [("#", 4, "right")] + self._columns
            lines.append(self._format_row([c[0] for c in effective], effective))
            lines.append("-" * self._width)
            if self._rows:
                for index, details in enumerate(self._rows, start=1):
                    lines.append(self._format_row([str(index)] + details, effective))
            else:
                lines.append(self._center(self._note))
        elif self._pairs:
            for label, value in self._pairs:
                lines.append(f" {label}: {value}".ljust(self._width))
        else:
            lines.append(self._center(self._note))
        lines.append("-" * self._width)
        if self._totals:
            lines.append(f" {self._totals}".ljust(self._width))
        lines.append("=" * self._width)
        lines.append(self._center(self._footer))
        lines.append("=" * self._width)
        return lines


class ReportBuilderFactory:
    # Complejidad: O(1)
    def __init__(self, width: int = CONTENT_WIDTH) -> None:
        self._width = width

    # Complejidad: O(1)
    def create(self) -> ReportBuilder:
        builder = ReportBuilder(self._width)
        builder.metadata("Generado", datetime.now().strftime(DATETIME_FORMAT))
        return builder
