from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.game.models import (
    Game,
    Player,
    GameScore,
    ChatModel,
    GameModel,
    PlayerModel,
    GameScoreModel
)

#TODO: change this shit totaly to be game_accessor

class GameAccessor(BaseAccessor):

    async def create_game(self, chat_id: int, players: list[Player]) -> Game:
        async with self.app.database.session() as session:
            players_list = [PlayerModel(chat_id=player.chat_id, telegram_id=player.telegram_id, 
                                        first_name=player.first_name, last_name=player.last_name,
                                        score=player.score, game=player.game) for player in players]
            game = GameModel(chat_id=chat_id, players=players_list)
            session.add(game)
            await session.commit()
            return game.to_data()
        
    async def create_player(self, chat_id: int, telegram_id: int, first_name: str, last_name: str, 
                            score: GameScore, game: Game) -> Player:
        async with self.app.database.session() as session:
            player = PlayerModel(chat_id=chat_id, telegram_id=telegram_id, first_name=first_name, last_name=last_name,
                                 score=score, game=game)
            session.add(player)
            await session.commit()
            return player.to_data()
        
    async def create_game_score(self, points: int, player: Player) -> GameScore:
        async with self.app.database.session() as session:
            game_score = GameScoreModel(points=points, player=player)
            session.add(game_score)
            await session.commit()
            return game_score.to_data()
        
    async def get_all_players_in_chat(self, chat_id: int) -> list[Player]:
        async with self.app.database.session() as session:
            q = select(PlayerModel).where(PlayerModel.chat_id == chat_id)
            result = await session.execute(q)
            players = result.scalars().all()
            if players:
                return [player.to_data() for player in players]

    async def get_latest_game_by_chat_id(self, chat_id: int) -> Game:
        async with self.app.database.session() as session:
            q = select(GameModel).where(GameModel.chat_id == chat_id).order_by(GameModel.created_at.desc())
            result = await session.execute(q)
            game = result.scalars().first()
            if game:
                return game.to_data()
            
    async def get_latest_players_by_chat_id(self, chat_id: int) -> list[Player]:
        async with self.app.database.session() as session:
            q = select(PlayerModel).where(PlayerModel.chat_id == chat_id).order_by(PlayerModel.game.created_at.desc())
            result = await session.execute(q)
            players = result.scalars().all()
            if players:
                return [player.to_data() for player in players]
            
    async def get_latest_scores_by_chat_id(self, chat_id: int) -> list[GameScore]:
        async with self.app.database.session() as session:
            q = select(GameScoreModel).where(GameScoreModel.player.chat_id == chat_id).order_by(GameScoreModel.player.game.created_at.desc())
            result = await session.execute(q)
            scores = result.scalars().all()
            if scores:
                return [score.to_data() for score in scores]

# class QuizAccessor(BaseAccessor):
#     async def create_theme(self, title: str) -> Theme:
#         async with self.app.database.session() as session:
#             theme = ThemeModel(title=title)
#             session.add(theme)
#             await session.commit()
#             return theme.to_data()

#     async def get_theme_by_title(self, title: str) -> Optional[Theme]:
#         async with self.app.database.session() as session:
#             q = select(ThemeModel).where(ThemeModel.title == title)
#             result = await session.execute(q)
#             theme = result.scalars().first()
#             if theme:
#                 return theme.to_data()

#     async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
#         async with self.app.database.session() as session:
#             q = select(ThemeModel).where(ThemeModel.id == id_)
#             result = await session.execute(q)
#             theme = result.scalars().first()
#             if theme:
#                 return theme.to_data()

#     async def list_themes(self) -> list[Theme]:
#         async with self.app.database.session() as session:
#             q = select(ThemeModel)
#             result = await session.execute(q)
#             themes = result.scalars().all()
#             return [theme.to_data() for theme in themes]

#     async def create_answers(self, question_id: int, answers: list[Answer]) -> list[Answer]:
#         pass

#     async def create_question(
#         self, title: str, theme_id: int, answers: list[Answer]
#     ) -> Question:
#         async with self.app.database.session() as session:
#             answers = [AnswerModel(title=answer.title, is_correct=answer.is_correct) for answer in answers]
#             question = QuestionModel(title=title, theme_id=theme_id, answers=answers)
#             session.add(question)
#             await session.commit()
#             return question.to_data()

#     async def get_question_by_title(self, title: str) -> Optional[Question]:
#         async with self.app.database.session() as session:
#             q = select(QuestionModel).where(QuestionModel.title == title).options(selectinload(QuestionModel.answers))
#             result = await session.execute(q)
#             question = result.scalars().first()
#             if question:
#                 return question.to_data()

#     async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
#         async with self.app.database.session() as session:
#             if theme_id:
#                 q = select(QuestionModel).where(QuestionModel.theme_id == theme_id)
#             else:
#                 q = select(QuestionModel)
#             result = await session.execute(q.options(selectinload(QuestionModel.answers)))
#             questions = result.scalars().all()
#             for q in questions:
#                 return [q.to_data() for q in questions]
