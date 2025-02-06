from flask import Flask, render_template, request, redirect, url_for
from app import app 

filmes = []
sessoes = []

@app.route('/')
def index():
    return render_template('index.html', filmes=filmes, sessoes=sessoes)

@app.route('/add_filme', methods=['POST'])
def add_filme():
    titulo = request.form['titulo']
    genero = request.form['genero']
    if titulo and genero:
        filmes.append({'titulo': titulo, 'genero': genero})
    return redirect(url_for('index'))

@app.route('/add_sessao', methods=['POST'])
def add_sessao():
    filme = request.form['filme']
    horario = request.form['horario']
    if filme and horario:
        sessoes.append({'filme': filme, 'horario': horario})
    return redirect(url_for('index'))
