from flask import render_template, Blueprint, url_for, request, flash, redirect
from models.cliente import Cliente

from flask_login import login_required, login_user, logout_user, current_user

# módulo de usuários
bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@bp.route('/')
def index():
    return render_template('clientes/index.html', clientes = Cliente.all())

@bp.route('/cadastrar_cliente', methods=['POST', 'GET'])
def cadastrar_cliente():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        nome=request.form['nome']

        if not email:
            flash('Email é obrigatório')
        else:
            Cliente.add_cliente(nome=nome,email=email,senha=senha)
            return redirect(url_for('clientes.index'))
    
    return render_template('clientes/cadastrar.html')



@bp.route('/login_cliente', methods=['GET', 'POST'])
def login_cliente():

    if current_user.is_authenticated:
        return redirect(url_for('clientes.index'))

    if request.method == 'GET':
        return render_template('clientes/login.html')
    else:
        email = request.form['email']
        senha = request.form['senha']
        cliente = Cliente.get_by_email(email)

        if cliente and cliente.senha == senha:
            login_user(cliente)
            return redirect(url_for('clientes.index'))
        else:
            flash('Dados incorretos.')
            return render_template('clientes/login.html')


@bp.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('clientes.index'))