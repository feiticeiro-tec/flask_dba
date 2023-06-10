"""Módulo de utilidades para as exceções."""""
from datetime import time
from . import TimeInvalidoException


def validate_time(_time):
    """Valida se o tempo é um objeto time."""
    if _time and not isinstance(_time, time):
        raise TimeInvalidoException(
            'O Tempo deve ser um objeto time.'
        )
