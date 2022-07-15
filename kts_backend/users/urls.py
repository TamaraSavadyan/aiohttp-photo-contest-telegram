from aiohttp.web_app import Application
from aiohttp_cors import CorsConfig

from ktstools.web.aiohttp.method import Method

from . import views

__all__ = ("register_urls",)


def register_urls(application: Application, cors: CorsConfig):
    cors.add(
        application.router.add_route(
            Method.GET,
            "/users/get",
            views.UserGet,
        ),
    )
