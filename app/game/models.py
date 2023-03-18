from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, BigInteger, DateTime, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


#TODO: Сделать нормальные relations, 'game' and 'player' is ManyToMany through 'chat'
#TODO: Посмотреть все on-delete=CASCADE и убрать где ненужно
#TODO: Исправить другие ошибки


@dataclass
class Game:
    id: int
    created_at: datetime
    chat_id: int
    players: list["Player"]


@dataclass
class Player:
    telegram_id: int
    chat_id: int
    first_name: str
    last_name: str
    score: "GameScore"


@dataclass
class Chat:
    id: int
    game: "Game"
    player: "Player"

@dataclass
class GameScore:
    id: int
    points: int


class GameModel(db):
    __tablename__ = "games"
    id = Column(BigInteger, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id', ondelete="CASCADE"))
    player_id = Column(Integer, ForeignKey('players.id', ondelete="CASCADE"))
    created_at = Column(DateTime)

    def to_data(self) -> Game:
        return Game(
            id=self.id, 
            created_at=self.created_at, 
            chat_id=self.chat_id,
            players=[player.to_data() for player in self.players]
        )


class PlayerModel(db):
    __tablename__ = "players"
    telegram_id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id', ondelete="CASCADE"))
    score_id = Column(Integer, ForeignKey('game_scores.id', ondelete="CASCADE"))

    def to_data(self) -> Player:
        return Player(
            telegram_id=self.telegram_id, 
            created_at=self.created_at, 
            chat_id=self.chat_id,
            first_name=self.first_name,
            last_name=self.last_name,
            score=self.score_id
        )


class ChatModel(db):
    __tablename__ = "chats"
    id = Column(BigInteger, primary_key=True)
    player_id = Column(Integer, ForeignKey('games.id', ondelete="CASCADE"))
    game_id = Column(Integer, ForeignKey('players.id', ondelete="CASCADE"))

    def to_data(self) -> Chat:
        return Chat(
            id=self.id,
            game=self.game_id,
            player=self.player_id
        )


class GameScoreModel(db):
    __tablename__ = "game_scores"
    id = Column(BigInteger, primary_key=True)
    points = Column(BigInteger, default=0)
    
    player_id = Column(Integer, ForeignKey('players.id', ondelete="CASCADE"), nullable=False)

    def to_data(self) -> GameScore:
        return GameScore(
            id=self.id,
            points=self.points
        )

