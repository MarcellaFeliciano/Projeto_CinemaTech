from flask import render_template, Blueprint, url_for, request, flash, redirect, session
from models.filme import Filme, Sessao

# módulo de usuários juhiugihihk
bp = Blueprint('filmes', __name__, url_prefix='/filmes')

@bp.route('/')
def index():
    if 'gerente' in session:
        gerente = session['gerente']
        return render_template('filmes/index.html', gerente=gerente,filmes = Filme.all(), sessoes = Sessao.all())
    elif 'user' in session:
        user = session['user']
        return render_template('filmes/index.html', user=user,filmes = Filme.all(), sessoes = Sessao.all())
    
    return render_template('filmes/index.html', filmes = Filme.all(), sessoes = Sessao.all())
  

@bp.route('/add_filme', methods=['POST','GET'])
def add_filme():
    if request.method == 'POST':
        titulo = request.form['titulo']
        genero = request.form['genero']
        duracao = request.form['duracao']
        if titulo and genero:
            Filme.add_filme(titulo=titulo, genero=genero, duracao=duracao)
            #filmes.append({'titulo': titulo, 'genero': genero})
        return redirect(url_for('filmes.index'))

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
