from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
