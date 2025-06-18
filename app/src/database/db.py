from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем движок базы данных (используем SQLite для простоты)
engine = create_engine("sqlite:///./test.db", echo=True)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Получить сессию базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_create():
    """Создать таблицы в базе данных"""
    Base.metadata.create_all(bind=engine) 