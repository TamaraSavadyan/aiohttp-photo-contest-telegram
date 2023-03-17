from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: Optional[int]
    title: str


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"
    id = Column(BigInteger, primary_key=True)
    title = Column(String, unique=True, nullable=False)

    questions = relationship("QuestionModel")

    def to_data(self) -> Theme:
        return Theme(
            id=self.id,
            title=self.title
        )


class QuestionModel(db):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id', ondelete="CASCADE"), nullable=False)

    def to_data(self) -> Question:
        return Question(
            id=self.id,
            title=self.title,
            theme_id=self.theme_id,
            answers=[answer.to_data() for answer in self.answers]
        )


class AnswerModel(db):
    __tablename__ = "answers"
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    question = relationship("QuestionModel", backref="answers")

    def to_data(self) -> Answer:
        return Answer(
            title=self.title,
            is_correct=self.is_correct,
        )

