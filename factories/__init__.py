"""Validadores de campos y contratos de la capa de creacion.

Los validadores viven en este paquete porque la validacion forma parte de la
creacion de entidades (Factory) y no requiere un modulo adicional.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime

from config.settings import DATE_FORMAT
from core.exceptions import ValidationError


class Validator(ABC):
    """Interfaz minima de validacion de un campo."""

    # Complejidad: O(1)
    @abstractmethod
    def validate(self, value: object) -> object:
        ...


class NotEmptyValidator(Validator):
    """Valida que un texto no este vacio."""

    # Complejidad: O(1)
    def __init__(self, field_name: str) -> None:
        self._field_name = field_name

    # Complejidad: O(n)
    def validate(self, value: object) -> str:
        text = str(value).strip()
        if not text:
            raise ValidationError(f"El campo '{self._field_name}' no puede estar vacio.")
        return text


class PositiveNumberValidator(Validator):
    """Valida que un valor sea numerico y mayor que cero."""

    # Complejidad: O(1)
    def __init__(self, field_name: str) -> None:
        self._field_name = field_name

    # Complejidad: O(1)
    def validate(self, value: object) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"El campo '{self._field_name}' debe ser numerico.")
        if number <= 0:
            raise ValidationError(f"El campo '{self._field_name}' debe ser mayor que 0.")
        return number


class DateValidator(Validator):
    """Valida que un texto sea una fecha con formato definido."""

    # Complejidad: O(1)
    def __init__(self, field_name: str, date_format: str = DATE_FORMAT) -> None:
        self._field_name = field_name
        self._date_format = date_format

    # Complejidad: O(n)
    def validate(self, value: object) -> date:
        text = str(value).strip()
        if not text:
            raise ValidationError(f"El campo '{self._field_name}' no puede estar vacio.")
        try:
            return datetime.strptime(text, self._date_format).date()
        except ValueError:
            raise ValidationError(
                f"El campo '{self._field_name}' debe tener formato {self._date_format}."
            )
