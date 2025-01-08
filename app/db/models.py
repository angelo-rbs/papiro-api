from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, null
from app.db.base import Base


class UserModel(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    username = Column('usename', String, unique=True, nullable=False)
    email = Column('email', String, unique=True, nullable=False)
    senha = Column('senha', String, nullable=False)
    criadoEm = Column('criadoEm', TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    ativo = Column('isAtivo', Boolean, default=True)
