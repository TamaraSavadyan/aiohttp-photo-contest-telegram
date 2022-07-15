from aiohttp import web
from aiohttp.abc import Request
from ktstools.web.aiohttp.misc import get_request_ctx
from sentry_sdk import add_breadcrumb


@web.middleware
async def auth_mw(request: Request, handler):
    from .app import ApiApplication

    app: ApiApplication = request.app
    ctx = get_request_ctx(request)
    # Extract user information here. JWT as an example
    # token, payload = await app.jwt.extract_token(request)
    # payload = payload or {}
    # ctx.data._jwt_token = token
    # ctx.data._jwt_payload = payload
    # ctx.user.id = payload.get('user_id')

    if ctx.user.id:
        add_breadcrumb(
            category="auth",
            message=f"user {ctx.user.id}",
            level="info",
        )
    return await handler(request)
