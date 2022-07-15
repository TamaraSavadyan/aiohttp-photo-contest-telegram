from marshmallow import Schema, fields

from kts_backend.web.view import BaseView

from ..schema import UserSchema


class UserGetQuerySchema(Schema):
    id = fields.Int(required=True)


class UserGet(BaseView):
    class Meta:
        tags = ["user"]
        query_schema = UserGetQuerySchema()
        response_schema = UserSchema()

    async def execute(self):
        return {"id": 42, "name": "ktstools"}
