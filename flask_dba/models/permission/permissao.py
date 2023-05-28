"""Modelo de permissao de rota."""
from sqlalchemy import Column, String, Boolean
from ..base import ModelBase


class Permissao(ModelBase):
    """Permissao de rota."""
    __tablename__ = 'Permissao'
    endpoint = Column(String(255), nullable=False)
    method = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    publico = Column(Boolean, default=False, nullable=False)
