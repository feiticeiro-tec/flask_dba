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
    with inst_agendamento.app.app_context():
        agenda = inst_agendamento.Agendamento()
        agenda.insert(
            dia=1,
            hora=1,
            minuto=1,
        )
        agenda.add()
        agenda.save()
