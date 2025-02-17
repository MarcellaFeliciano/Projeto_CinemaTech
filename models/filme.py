
from sqlalchemy.orm import Mapped, mapped_column
from database import db

class Filme(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column()
    genero: Mapped[str] = mapped_column()
    duracao: Mapped[str] = mapped_column()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_titulo(cls, titulo):
        return cls.query.filter_by(titulo=titulo).first()

    @classmethod
    def add_filme(cls, titulo, genero, duracao):
        filme = cls(titulo=titulo, genero=genero, duracao=duracao)
        db.session.add(filme)
        db.session.commit()

    @classmethod
    def edit_titulo(cls, id, titulo):
        filme = cls.get(id)
        filme.titulo = titulo
        db.session.commit()

class Sessao(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    filme_id: Mapped[str] = mapped_column() # adicionar chave estrangeira
    horario: Mapped[str] = mapped_column()
    sala: Mapped[str] = mapped_column()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def add_sessao(cls, filme_id, horario, sala):
        filme = cls(filme_id=filme_id, horario=horario, sala=sala)
        db.session.add(filme)
        db.session.commit()

    @classmethod
    def edit_filme_id(cls, id, filme_id):
        filme = cls.get(id)
        filme.filme_id = filme_id
        db.session.commit()

