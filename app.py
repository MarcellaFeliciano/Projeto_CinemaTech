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
            Genero(nome='Comédia'),
            Genero(nome='Animação'),
            Genero(nome='Terror'),
            Genero(nome='Aventura'),
            Genero(nome='Drama'),
            Genero(nome='Fantasia')
    ]
        
        for genero in novos_generos:
            if genero.nome not in generos_nomes:
                db.session.add(genero)

        # Comitar apenas se novos gêneros foram adicionados
        db.session.commit()

        # Adicionar filmes
        filmes_existentes = [
        {
            "titulo": "O Rei Leão",
            "generos": ['Animação'],
            "duracao": '118 min',
            "sinopse": "A versão em live-action do clássico da Disney, que segue a jornada de Simba, um leão que deve enfrentar seu destino como rei.",
            "classificacao": 'Livre',
            "data_lancamento": "2019-07-18",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "Vingadores: Ultimato",
            "generos": ['Ação', 'Ficção Científica'],
            "duracao": '181 min',
            "sinopse": "Os heróis restantes tentam reverter os danos causados por Thanos, que destruiu metade da vida no universo.",
            "classificacao": "12 anos",
            "data_lancamento": "2019-04-25",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "Frozen - Uma Aventura Congelante",
            "generos": ['Animação', 'Aventura', 'Fantasia'],
            "duracao": '102 min',
            "sinopse": "A princesa Anna parte em uma jornada com um grupo improvável para encontrar sua irmã Elsa, cuja magia congelante ameaça o reino.",
            "classificacao": 'Livre',
            "data_lancamento": "2013-11-27",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "Jurassic World",
            "generos": ['Ação', 'Aventura', 'Ficção Científica'],
            "duracao": '124 min',
            "sinopse": "Um parque de dinossauros é reaberto ao público, mas logo um novo dinossauro geneticamente modificado escapa, colocando todos em perigo.",
            "classificacao": "12 anos",
            "data_lancamento": "2015-06-12",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "Titanic",
            "generos": ['Drama', 'Romance'],
            "duracao": '195 min',
            "sinopse": "Durante o fatídico naufrágio do Titanic, um romance improvável surge entre Rose e Jack, dois passageiros de classes sociais distintas.",
            "classificacao": "12 anos",
            "data_lancamento": "1997-12-19",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "Matrix",
            "generos": ['Ação', 'Ficção Científica'],
            "duracao": '136 min',
            "sinopse": "Neo descobre que o mundo que conhece é uma simulação controlada por máquinas e se junta a um grupo para lutar pela liberdade da humanidade.",
            "classificacao": "14 anos",
            "data_lancamento": "1999-03-31",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
            "generos": ['Aventura', 'Fantasia'],
            "duracao": '178 min',
            "sinopse": "Um grupo de heróis é formado para destruir o Anel do Poder e derrotar o Senhor das Trevas, Sauron.",
            "classificacao": "12 anos",
            "data_lancamento": "2001-12-19",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "A Origem",
            "generos": ['Ação', 'Aventura', 'Ficção Científica'],
            "duracao": '148 min',
            "sinopse": "Um ladrão especializado em roubar segredos através dos sonhos é desafiado a implantar uma ideia na mente de um alvo.",
            "classificacao": "12 anos",
            "data_lancamento": "2010-07-16",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "Harry Potter e a Pedra Filosofal",
            "generos": ['Aventura', 'Fantasia'],
            "duracao": '152 min',
            "sinopse": "Um jovem menino descobre que é um bruxo e parte para Hogwarts, uma escola mágica, para aprender a controlar seus poderes.",
            "classificacao": 'Livre',
            "data_lancamento": "2001-11-10",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        },
        {
            "titulo": "Pantera Negra",
            "generos": ['Ação'],
            "duracao": '134 min',
            "sinopse": "T'Challa, o novo rei de Wakanda, deve enfrentar um inimigo que ameaça seu trono e a segurança de seu país.",
            "classificacao": "12 anos",
            "data_lancamento": "2018-02-15",
            "imagem": "avatar.jpg"  # Substitua pelo link da imagem
        }
    ]

        for filme_data in filmes_existentes:
            filme = Filme(
                titulo=filme_data["titulo"],
                duracao=filme_data["duracao"],
                sinopse=filme_data["sinopse"],
                classificacao=filme_data["classificacao"],
                data_lancamento=filme_data["data_lancamento"],
                imagem=filme_data["imagem"]
            )
            db.session.add(filme)
            db.session.commit()  # Comitar o filme adicionado

            # Associe o filme aos gêneros
            for nome in filme_data["generos"]:
                genero = db.session.query(Genero).filter_by(nome=nome).first()
                if genero:
                    genero.filmes.append(filme)

        # Comitar as associações de filmes com gêneros
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
    
    return render_template ('index.html',filmes = Filme.all(), sessoes = Sessao.all())