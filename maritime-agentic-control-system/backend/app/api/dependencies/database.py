from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

<<<<<<< HEAD
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {})
=======
engine = create_engine(str(settings.DATABASE_URL), connect_args={"check_same_thread": False} if str(settings.DATABASE_URL).startswith("sqlite") else {})
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()