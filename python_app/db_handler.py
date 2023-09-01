import logging
import os
import uuid
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from contextlib import contextmanager

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

def uuid_gen():
    return str(uuid.uuid4())

class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), default=uuid_gen, nullable=False)
    user_id = Column(Integer, nullable=False)

class DatabaseHandler:
    def __init__(self):
        self.MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD', "")
        self.MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', "my_database")
        self.MYSQL_URL = os.environ.get('MYSQL_URL', "localhost:3306")
        self.MYSQL_USER = os.environ.get('MYSQL_USER', "root")
        self.DATABASE_URL = f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_ROOT_PASSWORD}@{self.MYSQL_URL}/{self.MYSQL_DATABASE}'
        
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)

        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def add_session(self, user_id):
        with self.get_session() as session:
            new_state = Sessions(
                user_id=user_id,
            )

            session.add(new_state)
            session.commit()