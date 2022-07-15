from ktstools.settings import BaseSettings
from ktstools.monit.server import MonitMixin
from ktstools.setup.cli import ClickCommand

from kts_backend.metrics import init_monit
from kts_backend.store import Store


class BaseCommandMixin:
    def make_store(self, settings: BaseSettings):
        return Store(settings)

    async def on_store_connect(self):
        if self.connector:
            await self.connector.connect()

    async def prepare(self):
        await super().prepare()
        init_monit(getattr(self, "monit", None))


class BaseCommand(BaseCommandMixin, ClickCommand[Store]):
    _base_ = True


class BaseDaemon(MonitMixin, BaseCommand):
    _base_ = True
