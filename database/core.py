from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from env import DatabaseEnv

Base = declarative_base()

engine = create_async_engine(
    f"mysql+aiomysql://{DatabaseEnv.USERNAME}:{DatabaseEnv.PASSWORD}@{DatabaseEnv.HOST}:{DatabaseEnv.PORT}/{DatabaseEnv.DATABASE}",
    pool_size=1,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False,
    connect_args={"charset": "utf8mb4"},
)

scope = sessionmaker(bind=engine, class_=AsyncSession)
