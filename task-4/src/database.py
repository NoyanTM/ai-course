from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum
from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(engine)


@contextmanager
def get_session():
    with Session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error: {e}")
        finally:
            session.close()


def generate_uuid():
    return str(uuid4())


class Base(DeclarativeBase):
    pass


class TimeBasedMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now, default=datetime.now)


class Player(TimeBasedMixin, Base):
    __tablename__ = "player"
    
    id: Mapped[UUID] = mapped_column(String, primary_key=True, default=generate_uuid)
    telegram_user_id: Mapped[int] = mapped_column(unique=True)
    telegram_username: Mapped[str]
    
    game_sessions: Mapped[list["GameSession"]] = relationship(back_populates="player")


class Status(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    SUSPENDED = "SUSPENDED"


class GameSession(TimeBasedMixin, Base):
    __tablename__ = "game_session"
    
    id: Mapped[UUID] = mapped_column(String, primary_key=True, default=generate_uuid)
    status: Mapped[Status] = mapped_column(default=Status.ACTIVE)
    
    player_id: Mapped[str] = mapped_column(ForeignKey("player.id"))
    player: Mapped[Player] = relationship(back_populates="game_sessions")
    inventory: Mapped[dict[str, Any]] = mapped_column(JSON)
    # inventory: Mapped[list["Item"]] = relationship(back_populates="game_session")
    
    def __repr__(self) -> str:
        return (
            f"<GameSession("
            f"id={self.id!r}, "
            f"status={self.status!r}, "
            f"player_id={self.player_id!r}, "
            f"inventory={self.inventory!r}"
            f")>"
        )
    
# class Item(TimeBasedMixin, Base):
#     __tablename__ = "item"
    
#     id: Mapped[UUID] = mapped_column(String, primary_key=True, default=generate_uuid)
#     name: Mapped[str] = mapped_column(unique=True)
#     description: Mapped[str]
    
#     game_session_id: Mapped[str] = mapped_column(ForeignKey("game_session.id"))
#     game_session: Mapped[GameSession] = relationship("GameSession", back_populates="inventory")
