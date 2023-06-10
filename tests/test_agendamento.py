import pytest
from flask_dba.exceptions import (
    MinutoInvalidoException,
    HoraInvalidoException,
    DiaInvalidoException,
    TimeInvalidoException
)
from datetime import time


def test_init_agendamento(inst_f):
    """Testa a inicialização do agendamento."""
    with inst_f.app.app_context():
        inst_f.init_agendamento()
        inst_f.db.create_all()
        assert inst_f.Agendamento.query.all() == []
        assert inst_f.Coleta.query.all() == []
        assert inst_f.Credencial.query.all() == []
        assert inst_f.ExecucaoItem.query.all() == []
        assert inst_f.Execucao.query.all() == []


def test_add_agendamento(inst_agendamento):
    Ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = Ag()
        agenda.insert(
            dia=1,
            hora=2,
            minuto=3,
        )
        agenda.add()
        agenda.save()

    with inst_agendamento.app.app_context():
        agenda = Ag.query.first()
        assert agenda.dia == 1
        assert agenda.hora == 2
        assert agenda.minuto == 3


def test_raise_dia_invalido(inst_agendamento):
    Ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = Ag()
        with pytest.raises(DiaInvalidoException):
            agenda.insert(
                dia=32,
                hora=2,
                minuto=3,
            )


def test_raise_hora_invalido(inst_agendamento):
    Ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = Ag()
        with pytest.raises(HoraInvalidoException):
            agenda.insert(
                dia=1,
                hora=24,
                minuto=3,
            )


def test_raise_minuto_invalido(inst_agendamento):
    Ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = Ag()
        with pytest.raises(MinutoInvalidoException):
            agenda.insert(
                dia=1,
                hora=2,
                minuto=60,
            )


def test_raise_time_invalido(inst_agendamento):
    Ag = inst_agendamento.Agendamento
    with inst_agendamento.app.app_context():
        agenda = Ag()
        with pytest.raises(TimeInvalidoException):
            agenda.insert(
                dia=1,
                hora=2,
                minuto=60,
                _time='teste'
            )


def test_execucao(inst_agendamento):
    Ag = inst_agendamento.Agendamento
    Exe = inst_agendamento.Execucao
    agenda_uuid = None
    with inst_agendamento.app.app_context():
        agenda = Ag.query.first()
        agenda_uuid = agenda.uuid
        exe = agenda.add_execucao()
        exe.save()

    with inst_agendamento.app.app_context():
        exe = Exe.query.filter(
            Exe.agendamento_uuid == agenda_uuid
        ).first()
        assert exe is not None


def test_execucao_item(inst_agendamento):
    Exe = inst_agendamento.Execucao
    Item = inst_agendamento.ExecucaoItem
    with inst_agendamento.app.app_context():
        exe = Exe.query.first()
        item = exe.add_item(
            tempo_de_coleta=time(1, 35, 15)
        )
        item.save()

    with inst_agendamento.app.app_context():
        assert Item.query.first() is not None


def test_execucao_item_raise_tempo(inst_agendamento):
    Exe = inst_agendamento.Execucao
    with inst_agendamento.app.app_context():
        exe = Exe.query.first()
        with pytest.raises(TimeInvalidoException):
            exe.add_item(
                tempo_de_coleta='sadasd'
            )


def test_coleta(inst_agendamento):
    Coleta = inst_agendamento.Coleta
    with inst_agendamento.app.app_context():
        item = inst_agendamento.ExecucaoItem.query.first()
        coleta = item.add_coleta()
        coleta.save()

    with inst_agendamento.app.app_context():
        assert Coleta.query.first() is not None


def test_add_multime_coleta(inst_agendamento):
    Coleta = inst_agendamento.Coleta
    with inst_agendamento.app.app_context():
        item = inst_agendamento.ExecucaoItem.query.first()
        coleta = item.add_coleta()
        coleta = item.add_coleta()
        coleta.save()

    with inst_agendamento.app.app_context():
        assert len(Coleta.query.all()) == 3  # 2 + 1
