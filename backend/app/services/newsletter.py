from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from ..models import NewsletterSubscriber


def subscribe_email(session: Session, email: str) -> bool:
  """Subscribe an email address. Returns True if newly inserted"""
  normalized = email.strip().lower()
  stmt = (
      insert(NewsletterSubscriber)
      .values(email=normalized)
      .on_conflict_do_nothing(index_elements=[NewsletterSubscriber.email])
      .returning(NewsletterSubscriber.id)
  )
  result = session.execute(stmt)
  session.flush()
  return result.scalar_one_or_none() is not None


def get_recent_subscribers(session: Session, limit: int = 50) -> List[Dict[str, str]]:
  """Return a small sample of recent subscribers for debugging"""
  rows = session.execute(
      select(NewsletterSubscriber.email, NewsletterSubscriber.created_at)
      .order_by(NewsletterSubscriber.created_at.desc())
      .limit(limit)
  ).all()

  return [
    {"email": email, "created_at": created_at.isoformat()}
    for email, created_at in rows
  ]
