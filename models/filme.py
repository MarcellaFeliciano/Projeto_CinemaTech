
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Column, Table
from typing import List
from database import db


# Tabela associativa para o relacionamento muitos-para-muitos
filmes_generos = Table(
    'filmes_generos',
    db.Model.metadata,
    Column('filmes_id', ForeignKey('filme.id'), primary_key=True),
    Column('generos_id', ForeignKey('genero.id'), primary_key=True)
)


class Genero(db.Model):
    __tablename__ = 'genero'  # Adicionando o nome da tabela
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)  # Adicionando nullable=False

    # Relação com Filme
    #filmes: Mapped[List['Filme']] = relationship('Filme', secondary=filmes_generos, back_populates='generos')
    filmes = relationship('Filme', secondary=filmes_generos, back_populates='generos') # lista os alunos vinculados ao curso

    @classmethod
    def all(cls):
        return db.session.query(cls).all()


class Sessao(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    filme_id: Mapped[int] = mapped_column(ForeignKey('filme.id'), nullable=False)
    horario: Mapped[str] = mapped_column()
    data:  Mapped[str] = mapped_column()
    sala: Mapped[str] = mapped_column()

     # Relacionamento com Filme
    filme: Mapped['Filme']=relationship('Filme', back_populates='sessoes')
    
    @classmethod
    def all(cls):
        return db.session.query(cls).all()
    
    @classmethod
    def all_order(cls):
        return cls.query.join(Filme).order_by(Filme.titulo).all()

    @classmethod
    def get(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def add_sessao(cls, filme_id, horario, sala, data):
        sessao = cls(filme_id=filme_id, horario=horario,data=data, sala=sala)
        db.session.add(sessao)
        db.session.commit()

    @classmethod
    def edit_filme_id(cls, id, filme_id):
        filme = cls.get(id)
        filme.filme_id = filme_id
        db.session.commit()


class Filme(db.Model):
    __tablename__ = 'filme'  # Adicionando o nome da tabela
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(nullable=False)  # Adicionando nullable=False
    duracao: Mapped[str] = mapped_column(nullable=False)  # Adicionando nullable=False
    sinopse: Mapped[str] = mapped_column(nullable=False)
    classificacao: Mapped[int] = mapped_column(nullable=False)
    data_lancamento: Mapped[str] = mapped_column(nullable=False)
    imagem: Mapped[str] = mapped_column(nullable=False)

    # Relação com Genero
    generos: Mapped[List[Genero]] = relationship('Genero', secondary=filmes_generos, back_populates='filmes')

    # Relacionamento com Sessao
    sessoes: Mapped[List[Sessao]] = relationship('Sessao', back_populates='filme')

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
    def add_filme(cls, titulo, generos, duracao, sinopse, classificacao, data_lancamento, imagem):
        filme = cls(titulo=titulo, duracao=duracao, sinopse=sinopse, classificacao=classificacao, data_lancamento=data_lancamento, imagem=imagem)
        db.session.add(filme)
        db.session.commit()

        filme = db.session.query(cls).filter_by(titulo=titulo).first()
        # Associe o filme ao gênero
        for nome in generos:
            genero = db.session.query(Genero).filter_by(nome=nome).first()
            if genero:
                genero.filmes.append(filme)

        db.session.commit()

    @classmethod
    def edit_titulo(cls, id, titulo):
        filme = cls.get(id)
        filme.titulo = titulo
        db.session.commit()

