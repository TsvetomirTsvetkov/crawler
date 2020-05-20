from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, DateTime
from contextlib import contextmanager
from .settings import DB_NAME

engine = create_engine(f"sqlite:///{DB_NAME}")
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False)


class Database:
    @classmethod
    def build(self):
        Base.metadata.create_all(engine)


class Server(Base):
    __tablename__ = 'Server'
    server_id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer)
    added = Column(DateTime)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
