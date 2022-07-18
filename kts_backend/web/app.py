from typing import Sequence, Callable

from aiohttp.web import (
    Application as AiohttpApplication,
    View as AiohttpView,
    Request as AiohttpRequest,
)
from pyparsing import Optional


from kts_backend import __appname__, __version__
from .urls import register_urls



__all__ = ("ApiApplication",)


class Application(AiohttpApplication):
    config = None
    store = None
    database = None

