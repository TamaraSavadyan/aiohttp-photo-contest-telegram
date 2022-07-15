from typing import Sequence, Callable

import aiohttp_cors

from ktstools.collections.getters import path
from ktstools.context import Context
from ktstools.swagger.aiohttp import SwaggerAiohttp
from ktstools.web.aiohttp.application import Application
from ktstools.web.aiohttp.decorators import DEFAULT_SECURITY_SCHEME_NAME

from kts_backend import __appname__, __version__
from .mw import auth_mw
from .urls import register_urls


__all__ = ("ApiApplication",)


class ApiApplication(Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._swagger = SwaggerAiohttp(self, __appname__, __version__)
        self._swagger.add_security_scheme_bearer(DEFAULT_SECURITY_SCHEME_NAME)

        allowed_domains = path(
            self.config, "security", "cors_allowed_domains", default=[]
        )
        self.cors = aiohttp_cors.setup(
            self,
            defaults={
                domain: aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
                for domain in allowed_domains
            },
        )

        register_urls(self, self.cors)

    def get_middlewares(self) -> Sequence[Callable]:
        yield from super().get_middlewares()
        yield auth_mw
