from flask import render_template, Blueprint, url_for, request, flash, redirect, session, current_app
from models.filme import Filme, Sessao
from werkzeug.utils import secure_filename
import os

# módulo de usuários juhiugihihk
bp = Blueprint('filmes', __name__, url_prefix='/filmes')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/')
def index():
    if 'gerente' in session:
        gerente = session['gerente']
        return render_template('filmes/index.html', gerente=gerente,filmes = Filme.all(), sessoes = Sessao.all())
    elif 'user' in session:
        user = session['user']
        return render_template('filmes/index.html', user=user,filmes = Filme.all(), sessoes = Sessao.all())
    
    return render_template('filmes/index.html', filmes = Filme.all(), sessoes = Sessao.all())
  

@bp.route('/add_filme', methods=['POST', 'GET'])
def add_filme():
    if request.method == 'POST':
        titulo = request.form['titulo']
        genero = request.form['genero']
        duracao = request.form['duracao']
        
        # Processar o upload da imagem
        file = request.files.get('imagem')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']  # Use current_app para acessar a configuração
            file.save(os.path.join(upload_folder, filename))
            # Você pode salvar o caminho da imagem no banco de dados, se necessário.
            # Exemplo: Filme.add_filme(titulo=titulo, genero=genero, duracao=duracao, imagem=filename)
        
        Filme.add_filme(titulo=titulo, genero=genero, duracao=duracao)
        flash('Filme adicionado com sucesso!')
        return redirect(url_for('filmes.index'))

    else:
        return render_template('filmes/cadastrar_filme.html', filmes=Filme.all(), sessoes=Sessao.all())

@bp.route('/add_sessao', methods=['POST','GET'])
def add_sessao():
    if request.method == 'POST':
        filme = request.form['filme']
        horario = request.form['horario']
        sala = request.form['sala']
        if filme and horario and sala:

            Sessao.add_sessao(filme_id=filme, horario=horario, sala=sala)
            #sessoes.append({'filme': filme, 'horario': horario})
        return redirect(url_for('filmes.index'))
    
    else:
        return render_template('filmes/cadastrar_sessao.html', filmes = Filme.all(), sessoes = Sessao.all())

