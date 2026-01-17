from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from ..models import User


def create_user(session: Session, email: str, password: str) -> Optional[User]:
  normalized = email.strip().lower()
  password_hash = generate_password_hash(password)
  user = User(email=normalized, password_hash=password_hash)
  session.add(user)
  try:
    session.flush()
  except IntegrityError:
    session.rollback()
    return None
  return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
  normalized = email.strip().lower()
  user = session.scalar(select(User).where(User.email == normalized))
  if not user or not check_password_hash(user.password_hash, password):
    return None
  user.last_login_at = datetime.now(timezone.utc)
  session.flush()
  return user


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
  return session.get(User, user_id)
