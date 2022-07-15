from ktstools.context import Context
from ktstools.web.aiohttp.views.view import View

from kts_backend.store import Store
from .app import ApiApplication


class BaseView(View[ApiApplication, Store, Context]):
    pass
