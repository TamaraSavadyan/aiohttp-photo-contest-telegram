from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme,
    ThemeModel,
    QuestionModel,
    AnswerModel
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        async with self.app.database.session() as session:
            theme = ThemeModel(title=title)
            session.add(theme)
            await session.commit()
            return theme.to_data()

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        async with self.app.database.session() as session:
            q = select(ThemeModel).where(ThemeModel.title == title)
            result = await session.execute(q)
            theme = result.scalars().first()
            if theme:
                return theme.to_data()

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        async with self.app.database.session() as session:
            q = select(ThemeModel).where(ThemeModel.id == id_)
            result = await session.execute(q)
            theme = result.scalars().first()
            if theme:
                return theme.to_data()

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session() as session:
            q = select(ThemeModel)
            result = await session.execute(q)
            themes = result.scalars().all()
            return [theme.to_data() for theme in themes]

    async def create_answers(self, question_id: int, answers: list[Answer]) -> list[Answer]:
        pass

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        async with self.app.database.session() as session:
            answers = [AnswerModel(title=answer.title, is_correct=answer.is_correct) for answer in answers]
            question = QuestionModel(title=title, theme_id=theme_id, answers=answers)
            session.add(question)
            await session.commit()
            return question.to_data()

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        async with self.app.database.session() as session:
            q = select(QuestionModel).where(QuestionModel.title == title).options(selectinload(QuestionModel.answers))
            result = await session.execute(q)
            question = result.scalars().first()
            if question:
                return question.to_data()

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        async with self.app.database.session() as session:
            if theme_id:
                q = select(QuestionModel).where(QuestionModel.theme_id == theme_id)
            else:
                q = select(QuestionModel)
            result = await session.execute(q.options(selectinload(QuestionModel.answers)))
            questions = result.scalars().all()
            for q in questions:
                return [q.to_data() for q in questions]
