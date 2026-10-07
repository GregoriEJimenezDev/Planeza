"""Excepciones controladas del dominio Planexa."""


class PlanexaError(Exception):
    """Excepcion base controlada del sistema."""

    # Complejidad: O(1)
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ValidationError(PlanexaError):
    """Error de validacion de entrada."""


class DuplicateCodeError(PlanexaError):
    """Codigo de proyecto duplicado."""


class DuplicateTaskIdError(PlanexaError):
    """ID de tarea duplicado dentro del proyecto."""


class EmptyDequeError(PlanexaError):
    """Operacion sobre un deque vacio."""


class EntityNotFoundError(PlanexaError):
    """Entidad inexistente."""
