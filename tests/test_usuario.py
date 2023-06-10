"""Testes para o módulo de usuário."""


def test_create_usuario(session_usuario):
    """Testa a criação de um usuário."""
    _user = session_usuario.Usuario
    with session_usuario.app.app_context():
        user = _user()
        user.insert_credencial(
            username='teste',
            password='123456',
        )
        user.insert_contato(
            email='email@dominio.com'
        )
        user.add()
        user.save()

    with session_usuario.app.app_context():
        user = _user.query.first()
        assert user.email == 'email@dominio.com'
        assert user.username == 'teste'
        assert user.check_password('123456')
        assert user.admin is False


def test_bind_permissions_with_user(session_usuario):
    """Testa a associação de permissões com o usuário."""
    dba = session_usuario
    with dba.app.app_context():
        dba.init_permissions(
            usuario=True,
        )
        dba.db.create_all()
        dba.init_rules()

    with dba.app.app_context():
        assert dba.PermissaoUsuario.query.all() == []
        assert dba.Permissao.query.all() != []


def test_add_permissao_to_user(session_usuario):
    """Testa a adição de permissão ao usuário."""
    dba = session_usuario
    _puser = dba.PermissaoUsuario
    user_uuid = None
    permissao_uuid = None
    with dba.app.app_context():
        user = dba.Usuario.query.first()
        user_uuid = user.uuid
        permissao = dba.Permissao.query.first()
        permissao_uuid = permissao.uuid
        permissao.add_to_user(
            usuario_uuid=user.uuid
        )
        permissao.save()

    with dba.app.app_context():
        assert _puser.query.filter(
            _puser.usuario_uuid == user_uuid,
            _puser.permissao_uuid == permissao_uuid
        ).first() is not None
