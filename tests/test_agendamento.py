"""Testes para o módulo de agendamento."""
from datetime import time
import pytest
# pylint: disable=E0401
from flask_dba import FlaskDBA
from flask_dba.exceptions import (
    MinutoInvalidoException,
    HoraInvalidoException,
    DiaInvalidoException,
    TimeInvalidoException
)


def test_init_agendamento(inst_f: FlaskDBA):
    """Testa a inicialização do agendamento."""
    with inst_f.app.app_context():
        inst_f.init_agendamento()
        inst_f.db.create_all()
        assert inst_f.Agendamento.query.all() == []
        assert inst_f.Coleta.query.all() == []
        assert inst_f.Credencial.query.all() == []
        assert inst_f.ExecucaoItem.query.all() == []
        assert inst_f.Execucao.query.all() == []


def test_add_agendamento(inst_agendamento: FlaskDBA):
    """Testa a inserção de um agendamento."""
    _ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = _ag()
        agenda.insert(
            dia=1,
            hora=2,
            minuto=3,
        )
        agenda.add()
        agenda.save()

    with inst_agendamento.app.app_context():
        agenda = _ag.query.first()
        assert agenda.dia == 1
        assert agenda.hora == 2
        assert agenda.minuto == 3


def test_raise_dia_invalido(inst_agendamento: FlaskDBA):
    """Testa a exceção para o dia inválido."""
    _ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = _ag()
        with pytest.raises(DiaInvalidoException):
            agenda.insert(
                dia=32,
                hora=2,
                minuto=3,
            )


def test_raise_hora_invalido(inst_agendamento: FlaskDBA):
    """Testa a exceção para a hora inválida."""
    _ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = _ag()
        with pytest.raises(HoraInvalidoException):
            agenda.insert(
                dia=1,
                hora=24,
                minuto=3,
            )


def test_raise_minuto_invalido(inst_agendamento: FlaskDBA):
    """Testa a exceção para o minuto inválido."""
    _ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = _ag()
        with pytest.raises(MinutoInvalidoException):
            agenda.insert(
                dia=1,
                hora=2,
                minuto=60,
            )


def test_raise_time_invalido(inst_agendamento: FlaskDBA):
    """Testa a exceção para o tempo inválido."""
    _ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = _ag()
        with pytest.raises(TimeInvalidoException):
            agenda.insert(
                dia=1,
                hora=2,
                minuto=60,
                _time='teste'
            )


def test_execucao(inst_agendamento: FlaskDBA):
    """Testa a adição de uma execução."""
    _ag = inst_agendamento.Agendamento
    _exe = inst_agendamento.Execucao
    agenda_uuid = None
    with inst_agendamento.app.app_context():
        agenda = _ag.query.first()
        agenda_uuid = agenda.uuid
        exe = agenda.add_execucao()
        exe.save()

    with inst_agendamento.app.app_context():
        exe = _exe.query.filter(
            _exe.agendamento_uuid == agenda_uuid
        ).first()
        assert exe is not None


def test_execucao_item(inst_agendamento: FlaskDBA):
    """Testa a adição de um item na execução."""
    _exe = inst_agendamento.Execucao
    _item = inst_agendamento.ExecucaoItem
    with inst_agendamento.app.app_context():
        exe = _exe.query.first()
        item = exe.add_item(
            tempo_de_coleta=time(1, 35, 15)
        )
        item.save()

    with inst_agendamento.app.app_context():
        assert _item.query.first() is not None


def test_execucao_item_raise_tempo(inst_agendamento: FlaskDBA):
    """Testa a adição de um item com tempo inválido."""
    _exe = inst_agendamento.Execucao
    with inst_agendamento.app.app_context():
        exe = _exe.query.first()
        with pytest.raises(TimeInvalidoException):
            exe.add_item(
                tempo_de_coleta='sadasd'
            )


def test_coleta(inst_agendamento: FlaskDBA):
    """Testa a adição de uma coleta."""
    _coleta = inst_agendamento.Coleta
    with inst_agendamento.app.app_context():
        item = inst_agendamento.ExecucaoItem.query.first()
        coleta = item.add_coleta()
        coleta.save()

    with inst_agendamento.app.app_context():
        assert _coleta.query.first() is not None


def test_add_multime_coleta(inst_agendamento: FlaskDBA):
    """Testa a adição de múltiplas coletas."""
    _coleta = inst_agendamento.Coleta
    with inst_agendamento.app.app_context():
        item = inst_agendamento.ExecucaoItem.query.first()
        coleta = item.add_coleta()
        coleta = item.add_coleta()
        coleta.save()

    with inst_agendamento.app.app_context():
        assert len(_coleta.query.all()) == 3  # 2 + 1
