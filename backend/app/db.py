import os
import time
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

_engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker] = None


def _normalize_url(url: str) -> str:
  """Ensure the database URL uses the psycopg driver for SQLAlchemy"""
  if url.startswith("postgres://"):
    return "postgresql+psycopg://" + url[len("postgres://"):]
  if url.startswith("postgresql://") and "+psycopg" not in url:
    return "postgresql+psycopg://" + url[len("postgresql://"):]
  return url


def init_engine() -> Engine:
  """Create the SQLAlchemy engine and initialize tables"""
  global _engine, SessionLocal
  if _engine is not None and SessionLocal is not None:
    return _engine

  db_url = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://linkshort:linkshort@localhost:5432/linkshort"
  )
  db_url = _normalize_url(db_url)

  pool_size = max(1, int(os.getenv("DB_POOL_MAX", "10")))
  max_overflow = max(0, int(os.getenv("DB_MAX_OVERFLOW", "10")))

  engine = create_engine(
    db_url,
    pool_size=pool_size,
    max_overflow=max_overflow,
    future=True,
  )
  _engine = engine
  SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
  )

  retries = max(0, int(os.getenv("DB_CONNECT_RETRIES", "0")))
  retry_interval = max(0.0, float(os.getenv("DB_CONNECT_RETRY_INTERVAL", "1.0")))

  last_error: Optional[Exception] = None
  for attempt in range(retries + 1):
    try:
      Base.metadata.create_all(bind=engine)
      last_error = None
      break
    except OperationalError as exc:
      last_error = exc
      if attempt >= retries:
        break
      time.sleep(retry_interval)
  if last_error is not None:
    raise last_error
  return engine


@contextmanager
def session_scope() -> Generator[Session, None, None]:
  """Provide a transactional scope around a series of operations"""
  if SessionLocal is None:
    init_engine()
  assert SessionLocal is not None  # for type checkers
  session: Session = SessionLocal()
  try:
    yield session
    session.commit()
  except Exception:
    session.rollback()
    raise
  finally:
    session.close()
