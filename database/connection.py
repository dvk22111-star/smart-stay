from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://@"
    "(localdb)\\MSSQLLocalDB/"
    "smart_stay"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

print(SQLALCHEMY_DATABASE_URL)
import pyodbc

print(pyodbc.drivers())

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)