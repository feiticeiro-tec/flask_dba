"""Módulo de grupo de permissão."""
from sqlalchemy import Column, String
from ..base import ModelBase


class Grupo(ModelBase):
    """Grupo de permissão."""
    __tablename__ = 'Grupo'
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
