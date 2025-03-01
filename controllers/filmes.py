from flask import render_template, Blueprint, url_for, request, flash, redirect, session, current_app
from models.filme import Filme, Sessao, Genero
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
    
    return render_template('filmes/index.html', filmes = Filme.all(), sessoes = Sessao.all_order())
  
@bp.route('/add_filme', methods=['POST', 'GET'])
def add_filme():
    if request.method == 'POST':
        titulo = request.form['titulo']
        generos = request.form.getlist('generos')
        duracao = request.form['duracao']
        sinopse = request.form['sinopse']
        classificacao = request.form['classificacao']
        data_lancamento = request.form['data_lancamento']
        
       # Processar o upload da imagem
        file = request.files.get('file')
        filename = None  # Inicializa filename como None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            # Verifica se o diretório de uploads existe, caso contrário, cria
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            file.save(os.path.join(upload_folder, filename))
        
        # Adicionar o filme ao banco de dados
        Filme.add_filme(titulo=titulo, data_lancamento=data_lancamento, classificacao=classificacao,
                        sinopse=sinopse, generos=generos, duracao=duracao, imagem=filename)
        
        flash('Filme adicionado com sucesso!')
        return redirect(url_for('filmes.index'))

    else:
        return render_template('filmes/cadastrar_filme.html', filmes=Filme.all(), sessoes=Sessao.all(), generos=Genero.all())



@bp.route('/add_sessao', methods=['POST','GET'])
def add_sessao():
    if request.method == 'POST':
        filme = request.form['filme']
        data = request.form['data']
        horario = request.form['horario']
        sala = request.form['sala']
            
        Sessao.add_sessao(filme_id=filme, data=data, horario=horario, sala=sala)
            
        return redirect(url_for('filmes.index'))
    
    else:
        return render_template('filmes/cadastrar_sessao.html', filmes = Filme.all(), sessoes = Sessao.all())

