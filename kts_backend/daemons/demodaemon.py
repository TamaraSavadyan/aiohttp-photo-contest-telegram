import asyncio

from kts_backend.commands import BaseDaemon


class DemoDaemon(BaseDaemon):
    name = "demodaemon"

    @property
    def accessors(self):
        yield self.store.user

    async def execute(self):
        await self.connector.wait_connected()

        while self.is_running:
            self.logger.info("Daemon is running")
            await asyncio.sleep(1.0, loop=self.loop)
