import os

from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DataAccessLayer:

    def __init__(self):
        sql_dabatase_url: URL = URL.create(
            'postgresql+psycopg2',
            username=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB')
        )
        self.engine = create_engine(
            sql_dabatase_url,
            pool_pre_ping=True,
            pool_size=30,
            max_overflow=120
        )
        self.session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_session(self) -> Session:
        db = self.session()
        db.expire_on_commit = False
        try:
            yield db
        except Exception as e:
            raise e
        finally:
            db.close()

    def create_tables(self):
        Base.metadata.create_all(self.engine)
