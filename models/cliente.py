from flask_login import UserMixin, login_user
from sqlalchemy.orm import Mapped, mapped_column
from database import db

class Cliente(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str] = mapped_column()

    @classmethod
    def find(cls, **kwargs):
        if 'nome' in kwargs:
            return db.session.query(cls).filter_by(nome=kwargs['nome']).first()
        elif 'id' in kwargs:
            return db.session.query(cls).filter_by(id=kwargs['id']).first()
        else:
            raise AttributeError('A busca deve ser feita por nome ou id.')

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def add_cliente(cls, nome, email, senha):
        cliente = cls(nome=nome, email=email, senha=senha)
        db.session.add(cliente)
        db.session.commit()
        login_user(cliente)

    @classmethod
    def edit_email(cls, id, email):
        cliente = cls.get(id)
        cliente.email = email
        db.session.commit()