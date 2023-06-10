"""Modelo de agendamento para o scheduler."""
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from ..base import ModelBase


class Agendamento(ModelBase):
    """Agendamento para o scheduler."""
    __tablename__ = 'Agendamento'

    dia = Column(Integer, nullable=False)
    hora = Column(Integer, nullable=False)
    minuto = Column(Integer, nullable=False)

    credencial_uuid = Column(
        String(36),
        ForeignKey("Credencial.uuid"),
        nullable=True
    )
    credencial = declared_attr(
        lambda cls: relationship(
            'Credencial', backref='Agendamento',
        ))

    def insert(self, dia, hora, minuto):
        self.dia = dia
        self.hora = hora
        self.minuto = minuto

    def insert_credencial(self, credencial):
        self.credencial = credencial
        self.credencial_uuid = credencial.uuid
