from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.Core.Config.settings import settings

Base = declarative_base()

createdSessions = []

class ApplicationDatabaseContext:
    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            echo=settings.DATABASE_ECHO,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_db(self)-> Generator[Session, None, None]:
        db = self.SessionLocal()
        try:
            createdSessions.append(db)
            yield db
        finally:
            db.close()
