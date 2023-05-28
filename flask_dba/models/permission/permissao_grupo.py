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

    @staticmethod
    def permissoes_com_grupo_sem_match(cls, permissao, grupo, db):
        """Retorna as permissões que não possuem
        relacao com grupo correspondente.

        SELECT P.uuid, G.uuid
        FROM Permissao P
            LEFT JOIN PermissaoGrupo PG ON
                P.uuid == PG.permissao_uuid
            LEFT JOIN Grupo G ON
                PG.grupo_uuid == G.uuid
                AND G.custom == 0
        WHERE
            P.endpoint == G.nome
            AND P.custom == 0
            AND P.excludo == 0
            AND PG.uuid IS NULL

        """
        return db.session.query(permissao.uuid, grupo.uuid).join(
            cls, (
                permissao.uuid == cls.permissao_uuid
                and grupo.uuid == cls.grupo_uuid
            ), isouter=True
        ).filter(
            permissao.endpoint == grupo.nome,
            permissao.custom == 0,
            grupo.custom == 0,
            permissao.excludo == 0,
            grupo.excludo == 0,
            cls.uuid.is_(None),
        ).all()

    @staticmethod
    def gerar_relacoes(cls, permissao, grupo, db):
        """Gera as relações entre permissão e grupo."""
        for match in cls.permissoes_com_grupo_sem_match(
                cls, permissao, grupo, db):
            permissao_grupo = cls(
                permissao_uuid=match[0],
                grupo_uuid=match[1],
            )
            permissao_grupo.add(db)
        db.session.commit()
