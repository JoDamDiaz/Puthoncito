from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

# Prioridad de resolución de conexión:
# 1. MYSQL_URL / DATABASE_URL  (Railway plugin — URL completa)
# 2. MYSQLHOST / MYSQLPORT … (Railway plugin — variables individuales sin guión)
# 3. DB_HOST / DB_PORT …     (variables locales del .env)
_url = os.getenv("MYSQL_URL") or os.getenv("DATABASE_URL")
if _url:
    DATABASE_URL = _url.replace("mysql://", "mysql+pymysql://", 1)
else:
    host = os.getenv("MYSQLHOST") or os.getenv("DB_HOST")
    port = os.getenv("MYSQLPORT") or os.getenv("DB_PORT")
    user = os.getenv("MYSQLUSER") or os.getenv("DB_USER")
    password = os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASSWORD")
    database = os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME")
    DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
