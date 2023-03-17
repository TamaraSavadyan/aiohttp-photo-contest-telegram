from aiohttp_apispec import querystring_schema, request_schema, response_schema, docs
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest

from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.quiz.models import Answer
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @docs(tags=["vk_quiz"], summary="Add theme", description="Add theme in quiz")
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]
        if await self.store.quizzes.get_theme_by_title(title):
            raise HTTPConflict(reason='That theme already exist')
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags=["vk_quiz"], summary="Add question", description="Add question in quiz")
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        data = self.request["data"]
        data1 = await self.request.json()
        answers = data1['answers']

        flag = 0
        for answer in answers:
            if answer['is_correct'] == True:
                flag += 1
            if flag > 1:
                raise HTTPBadRequest
            
        if flag == 0:
                raise HTTPBadRequest    
            
        if len(answers) == 1:
            raise HTTPBadRequest
        
        if await self.store.quizzes.get_question_by_title(data["title"]):
            raise HTTPConflict
        if not await self.store.quizzes.get_theme_by_id(int(data["theme_id"])):
            raise HTTPNotFound
        question = await self.store.quizzes.create_question(
            title=data["title"],
            theme_id=data["theme_id"],
            answers=[
                Answer(
                    title=answer["title"],
                    is_correct=answer["is_correct"]
                ) for answer in data["answers"]
            ]
        )
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @docs(tags=["vk_quiz"], summary="Get question list", description="Get question list")
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        if self.request.query.get("theme_id"):
            theme_id = int(self.request.query.get("theme_id"))
        else:
            theme_id = None
        questions = await self.store.quizzes.list_questions(
            theme_id=theme_id
        )
        questions = [] if questions is None else questions
        return json_response(ListQuestionSchema().dump({"questions": questions}))
