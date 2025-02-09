from flask import render_template, Blueprint, url_for, request, flash, redirect, session
from models.gerente import Gerente


# módulo de usuários
bp = Blueprint('gerentes', __name__, url_prefix='/gerentes')

@bp.route('/')
def index():
    return render_template('gerentes/index.html', gerentes = Gerente.all())


@bp.route('/login_gerente', methods=['GET', 'POST'])
def login_gerente():

    if request.method == 'GET':
        return render_template('gerentes/login.html')
    else:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        gerente = Gerente.get_by_email(email)

        if gerente and gerente.senha == senha:
            session['gerente'] = nome
            return redirect(url_for('gerentes.index'))
        else:
            flash('Dados incorretos.')
            return render_template('gerentes/login.html')


@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    if session['gerente']:
        session.pop('gerente', None) 
        return redirect(url_for('gerentes.index'))