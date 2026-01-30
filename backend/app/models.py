from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
  pass


class ShortURL(Base):
  __tablename__ = "short_urls"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  short_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
  original_url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
  created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), server_default=func.now(), nullable=False
  )


class NewsletterSubscriber(Base):
  __tablename__ = "newsletter_subscribers"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
  created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), server_default=func.now(), nullable=False
  )

