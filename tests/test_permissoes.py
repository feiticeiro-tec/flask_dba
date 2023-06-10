"""Testes para as permissões."""
import pytest
from sqlalchemy.exc import OperationalError


def test_init_permissions(inst_f):
    """Testa a inicialização das permissões."""
    with inst_f.app.app_context():
        with pytest.raises(AttributeError):
            inst_f.Permissao.query.all()
        inst_f.init_permissions()
        with pytest.raises(OperationalError):
            inst_f.Permissao.query.all()
        inst_f.db.create_all()
        assert inst_f.Permissao.query.all() == []


def test_init_rules(inst_f):
    """Testa a inicialização das regras."""
    with inst_f.app.app_context():
        inst_f.init_permissions()
        inst_f.db.create_all()
        inst_f.init_rules()
        assert inst_f.Permissao.query.all() != []
