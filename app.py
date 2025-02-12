from flask import Flask, request, render_template, url_for, session

from controllers import clientes
from models.cliente import Cliente
from flask_login import LoginManager

from database import db

app = Flask(__name__)
"""
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return db.get(Cliente, user_id)
"""
login_manager = LoginManager()
@login_manager.user_loader #Carregador padrão do flask_login, isso é obrigatório
def load_user(user_id):
    return Cliente.find(id=user_id) #Pega o usuario baseado no ID, por meio dos kwargs (explicado na linha 32 e 33)
    #Esse função find está sendo definida la na linha 31, caso mude o nome la, tem que mudar aqui também

app.config['SECRET_KEY'] = 'muitodificil'

# Inicializa o controle de sessões
login_manager.init_app(app)



# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()     
                                                                                  
app.register_blueprint(clientes.bp)

@app.route ('/')
def index ():
    return render_template ('index.html')