from hashlib import sha256

from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response
from app.web.mixins import AuthRequiredMixin


class AdminLoginView(View):
    @docs(tags=["vk_quiz"], summary="Sign in", description="Sign in as Admin")
    @request_schema(AdminSchema)
    @response_schema(AdminSchema)
    async def post(self):
        data = self.request["data"]
        admin = await self.store.admins.get_by_email(data["email"])

        if not admin:
            raise HTTPForbidden(reason='no admin with this email')
        print(f'log {admin.password = }')
        print(f'log {sha256(self.data["password"].encode()).hexdigest() = }')
        if admin.password != sha256(self.data["password"].encode()).hexdigest():
            raise HTTPForbidden(reason='invalid password')

        raw_admin = AdminSchema().dump(admin)
        session = await new_session(request=self.request)
        session["admin"] = raw_admin
        return json_response(data=raw_admin)


class AdminCurrentView(AuthRequiredMixin, View):
    @docs(tags=["vk_quiz"], summary="Current admin", description="Current admin")
    @response_schema(AdminSchema, 200)
    async def get(self):
        return json_response(data=AdminSchema().dump(self.request.admin))
