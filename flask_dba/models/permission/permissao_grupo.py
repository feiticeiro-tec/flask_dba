"""Módulo de permissão de grupo."""
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..base import ModelBase


class PermissaoGrupo(ModelBase):
    """Permissão de grupo."""
    __tablename__ = 'PermissaoGrupo'
    grupo_uuid = Column(String(36), ForeignKey("Grupo.uuid"), nullable=False)
    grupo = declared_attr(lambda cls: relationship(
        'Grupo', backref='PermissaoGrupo',
    ))

    permissao_uuid = Column(
        String(36), ForeignKey("Permissao.uuid"), nullable=False)
    permissao = declared_attr(lambda cls: relationship(
        'Permissao', backref='PermissaoGrupo',
    ))
