from ktstools.context import Context
from ktstools.store import Accessor

from kts_backend.store import Store


class UserAccessor(Accessor[Store, None]):
    class Meta:
        name = "user"

    async def get(self, ctx: Context):
        return None
