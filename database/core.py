from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from env import DatabaseEnv

Base = declarative_base()

engine = create_engine(
    f"mysql+pymysql://{DatabaseEnv.USERNAME}:{DatabaseEnv.PASSWORD}@{DatabaseEnv.HOST}:{DatabaseEnv.PORT}/{DatabaseEnv.DATABASE}",
    encoding="utf-8",
    pool_size=40,
    max_overflow=60,
    pool_pre_ping=True,
)

factory = sessionmaker(bind=engine)


@contextmanager
def scope():
    session = factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
