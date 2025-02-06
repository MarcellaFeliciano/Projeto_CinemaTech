
from sqlalchemy.orm import Mapped, mapped_column
from app import db

conn = db

class Cliente(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]

    def all():
        clientes = conn.session.execute(conn.select(Cliente)).scalars()
        return clientes

    def get_user(id):
        cliente = Cliente.query.get_or_404(id)  
        return cliente


    def add_cliente(email,senha):
        cliente = Cliente(email=email,senha=senha,)
        conn.session.add(cliente)
        conn.session.commit()

            
    def edit_email(id,email):
        cliente = Cliente.get_Cliente(id)
        cliente.email = email
        conn.session.commit() 