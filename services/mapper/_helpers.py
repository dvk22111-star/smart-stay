from typing import Any


class DummyService:
    """Minimal service implementation used to satisfy API imports during setup."""

    async def _list(self, item: Any):
        return [item]

    async def _item(self, item: Any):
        return item

    async def _empty_list(self):
        return []

    async def _empty_dict(self):
        return {}
