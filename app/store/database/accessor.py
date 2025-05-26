from aiohttp import web
from app.forum.models import Message
from app.store.database.models import db

class PostgresAccessor:
    def __init__(self) -> None:
        # здесь был импорт Мессадж
        self.message = Message
        self.db = None

    def setup(self, application: web.Application) -> None:
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application: web.Application):
        # здесь был импорт дб
        self.config = application["config"]["postgres"]
        await db.set_bind(self.config["postgres"]["database_url"])
        self.db = db

    async def _on_disconnect(self, _) -> None:
        if self.db is not None:
            await self.db.pop_bind().close()