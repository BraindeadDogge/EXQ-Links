import secrets
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models import ShortURL


def generate_short_id(length: int = 6) -> str:
  """Generate a short id comprised of hex characters."""
  return secrets.token_hex(length // 2).upper()


def get_or_create_short_id(session: Session, original_url: str) -> str:
  """Fetch an existing mapping or insert a new short id."""
  existing = session.scalar(
      select(ShortURL.short_id).where(ShortURL.original_url == original_url)
  )
  if existing:
    return existing

  while True:
    short_id = generate_short_id()
    short_url = ShortURL(short_id=short_id, original_url=original_url)
    session.add(short_url)
    try:
      session.flush()
      return short_id
    except IntegrityError:
      session.rollback()
      existing = session.scalar(
          select(ShortURL.short_id).where(ShortURL.original_url == original_url)
      )
      if existing:
        return existing
      continue


def resolve_short_id(session: Session, short_id: str) -> Optional[str]:
  return session.scalar(
      select(ShortURL.original_url).where(ShortURL.short_id == short_id)
  )


def dump_store(session: Session) -> List[Dict[str, str]]:
  rows = session.execute(
      select(ShortURL.short_id, ShortURL.original_url, ShortURL.created_at)
      .order_by(ShortURL.created_at.desc())
      .limit(100)
  ).all()

  result: List[Dict[str, str]] = []
  for short_id, original_url, created_at in rows:
    created_at_iso = created_at.isoformat() if isinstance(
      created_at, datetime) else str(created_at)

    result.append(
      {
        "short_id": short_id,
        "original_url": original_url,
        "created_at": created_at_iso,
      }
    )
  return result
