from flask import Flask, request, render_template, url_for, session

from controllers import clientes, filmes, gerentes
from models.cliente import Cliente
from models.filme import Filme, Sessao, Genero
from models.gerente import Gerente
from flask_login import LoginManager
import os
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
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16 MB

# Inicializa o controle de sessões
login_manager.init_app(app)


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension


db.init_app(app)
with app.app_context():
    db.create_all()     
    existing_gerente = db.session.query(Gerente).filter_by(email='admin@admin.com').first()
    if existing_gerente:
        print("E-mail já cadastrado.")
    else:
        # Inserir novo gerente
        novo_gerente = Gerente(email='admin@admin.com', senha='123')
        db.session.add(novo_gerente)
        db.session.commit()

    count = Filme.query.count()
    if count == 0:
        # Verificar se os gêneros já existem
        generos_existentes = Genero.query.all()
        generos_nomes = {g.nome for g in generos_existentes}  # Conjunto com os nomes dos gêneros existentes

        # Criar novos gêneros apenas se não existirem
        novos_generos = [
            Genero(nome='Ficção Científica'),
            Genero(nome='Ação'),
            Genero(nome='Romance'),
            Genero(nome='Comedia'),
            Genero(nome='Terror')
        ]
        
        for genero in novos_generos:
            if genero.nome not in generos_nomes:
                db.session.add(genero)

        # Comitar apenas se novos gêneros foram adicionados
        if db.session.new:
            db.session.commit()





app.register_blueprint(clientes.bp)
app.register_blueprint(filmes.bp)
app.register_blueprint(gerentes.bp)

@app.route ('/')
def index ():
    if 'gerente' in session:
        gerente = session['gerente']
        return render_template('index.html', gerente=gerente,filmes = Filme.all(), sessoes = Sessao.all())
    elif 'user' in session:
        user = session['user']
        return render_template('index.html', user=user,filmes = Filme.all(), sessoes = Sessao.all())
    
    return render_template ('index.html')