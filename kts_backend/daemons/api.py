from typing import Iterable

from aiohttp.abc import Application
from ktstools.store.accessor import Accessor
from ktstools.web.aiohttp.daemon import BaseApiDaemon

from kts_backend.commands import BaseCommandMixin
from kts_backend.store import Store
from kts_backend.web.app import ApiApplication


class ApiDaemon(BaseCommandMixin, BaseApiDaemon[Store]):
    def create_app(self) -> Application:
        return ApiApplication(self.settings, self.store, connector=self.connector)

    @property
    def accessors(self) -> Iterable[Accessor]:
        pass
