from kts_backend.commands import BaseCommand


class DemoCommand(BaseCommand):
    name = "democmd"

    @property
    def accessors(self):
        yield self.store.user

    async def execute(self):
        await self.connector.wait_connected()
        self.logger.info("Command run")
