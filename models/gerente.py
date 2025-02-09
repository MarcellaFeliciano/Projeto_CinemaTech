
from sqlalchemy.orm import Mapped, mapped_column
from database import db

class Gerente(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str] = mapped_column()

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
    def add_gerente(cls, nome, email, senha):
        gerente = cls(nome=nome, email=email, senha=senha)
        db.session.add(gerente)
        db.session.commit()

    @classmethod
    def edit_email(cls, id, email):
        gerente = cls.get(id)
        gerente.email = email
        db.session.commit()