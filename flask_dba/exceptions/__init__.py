"""Módulo de exceções para o pacote flask_dba."""


class AgendamentoException(Exception):
    """Classe base para exceções neste módulo."""
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class DiaInvalidoException(AgendamentoException):
    """Exceção para o dia inválido."""
    def __init__(self, *args, **kw):
        super(AgendamentoException, self).__init__(*args, **kw)


class MinutoInvalidoException(AgendamentoException):
    """Exceção para o minuto inválido."""
    def __init__(self, *args, **kw):
        super(AgendamentoException, self).__init__(*args, **kw)


class HoraInvalidoException(AgendamentoException):
    """Exceção para a hora inválida."""
    def __init__(self, *args, **kw):
        super(AgendamentoException, self).__init__(*args, **kw)


class TimeInvalidoException(AgendamentoException):
    """Exceção para o tempo inválido."""
    def __init__(self, *args, **kw):
        super(AgendamentoException, self).__init__(*args, **kw)
