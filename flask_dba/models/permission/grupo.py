"""Módulo de grupo de permissão."""
from sqlalchemy import Column, String, Boolean
from ..base import ModelBase


class Grupo(ModelBase):
    """Grupo de permissão."""
    __tablename__ = 'Grupo'
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    custom = Column(Boolean, default=False, nullable=False)
