from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    String,
    Boolean,
    ForeignKey,
    Integer,
    func,
)

from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Game:
    id: int
    created_at: datetime
    chat_id: int
    players: list["Player"]


@dataclass
class Player:
    id: int
    telegram_id: int
    chat_id: int
    first_name: str
    last_name: str
    score: "GameScore"


@dataclass
class GameScore:
    id: int
    points: int
    player: "Player"


# class ChatModel(db):
#     __tablename__ = "chats"
#     id = Column(BigInteger, primary_key=True)

#     chat_id = Column(BigInteger)

#     player_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"))
#     game_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"))


class GameModel(db):
    __tablename__ = "games"
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chat_id = Column(BigInteger, nullable=False)

    players = relationship("PlayerModel", backref="games")

    # chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"))

    # players = relationship("PlayerModel", secondary="chats", backref="players")

    def to_data(self) -> Game:
        return Game(
            id=self.id,
            created_at=self.created_at,
            chat_id=self.chat_id,
            players=[player.to_data() for player in self.players],
        )


class PlayerModel(db):
    __tablename__ = "players"
    id = Column(BigInteger, primary_key=True)

    telegram_id = Column(BigInteger, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    chat_id = Column(BigInteger, nullable=False)
    # chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"))

    score = relationship("GameScoreModel", backref="players")
    game = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"))
    # games = relationship("GameModel", secondary="chats", backref="games")

    def to_data(self) -> Player:
        return Player(
            id=self.id,
            telegram_id=self.telegram_id,
            first_name=self.first_name,
            last_name=self.last_name,
            chat_id=self.chat_id,
            score=self.score,
        )


class GameScoreModel(db):
    __tablename__ = "game_scores"
    id = Column(BigInteger, primary_key=True)

    points = Column(BigInteger, default=0)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"))

    def to_data(self) -> GameScore:
        return GameScore(points=self.points)
