from flask_dba import FlaskDBA
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pytest import fixture


def instancia():
    """Instancia o app, db e dba."""
    app = Flask(import_name=__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app=app)
    dba = FlaskDBA(app=app, db=db)
    return dba


@fixture(scope='function')
def inst_f():
    """retona a instancia do dba."""
    return instancia()


@fixture(scope='session')
def inst_agendamento():
    dba = instancia()
    with dba.app.app_context():
        dba.init_agendamento()
        dba.db.create_all()
    return dba


@fixture(scope='session')
def inst_s():
    """Retorna a instancia do app, db e dba."""
    return instancia()


@fixture(scope='session')
def session_usuario():
    """Retorna a instancia do app, db e dba."""
    dba = instancia()
    with dba.app.app_context():
        dba.init_usuario()
        dba.db.create_all()
    return dba
