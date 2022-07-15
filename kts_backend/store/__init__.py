from ktstools.store import Store as BaseStore


class Store(BaseStore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from kts_backend.users.accessor import UserAccessor

        self.user = UserAccessor(self)
