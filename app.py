from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dba import FlaskDBA


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

dba = FlaskDBA()
dba.init_app(app, db)
dba.init_usuario()
dba.init_permissions(
    with_usuario=True
)
dba.init_agendamento()
dba.init_endereco(
    with_usuario=True
)
dba.init_empresa(
    with_endereco=True,
    with_colaborador=True,
    with_permissions=True
)
with app.app_context():
    db.create_all()
