import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _build_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    print(database_url)
    if database_url:
        return database_url

    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_NAME", "SMART_STAY")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if username and password:
        return (
            f"mssql+pyodbc://{quote_plus(username)}:{quote_plus(password)}@"
            f"{server}/{database}?driver={quote_plus(driver)}"
        )

    return "sqlite:///./smart_stay.db"


SQLALCHEMY_DATABASE_URL = _build_database_url()

connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)