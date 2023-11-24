""" Database setup and connection """

# pylint: disable=import-error
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import (
    db_user,
    db_password,
    db_host,
    db_port,
    db_name,
    environment,
)

if environment != 'production':
    DATABASE_URL = 'sqlite:///./chatdb.db'

    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

else:
    DATABASE_URL = f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(
        DATABASE_URL
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """ Functionto get a database connection.
    Returns:
        sqlalchemy.orm.session.Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
