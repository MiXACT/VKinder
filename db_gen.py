import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import psycopg2


def get_db_info():
    db_init = {}
    db_init['db'] = input('Наименование БД для хранения результатов поиска: ')
    db_init['password'] = input('Пароль от БД: ')
    engine = sq.create_engine(f"postgresql+psycopg2://postgres:{db_init['password']}@localhost:5432/{db_init['db']}")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return db_init

Base = declarative_base()

class Candidates(Base):
    __tablename__ = 'candidates'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)
    link = sq.Column(sq.String, nullable=False, unique=True)
    photos = relationship('Photos')

class Photos(Base):
    __tablename__ = 'photos'
    id = sq.Column(sq.Integer, primary_key=True)
    link = sq.Column(sq.String, nullable=False, unique=True)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.id'))