import aiohttp_jinja2
import gino
from aiohttp import web
from datetime import datetime
#создаем новый View
from app.forum.models import Message
from app.store.database.models import db
# создаем функцию, которая будет отдавать html-файл
@aiohttp_jinja2.template("index.html")
async def index(request):
   return {'title': 'Пишу первое приложение на aiohttp'}

class ListMessageView(web.View):
    async def get(self):
        messages = await Message.query.order_by(Message.id.desc()).gino.all()
        messages_data = []
        for message in messages:
            messages_data.append({
                "id": message.id,
                "text": message.text,
                "created": str(message.created),
            })

        return web.json_response(data={'messages': messages_data})
        

class CreateMessageView(web.View):
    async def post(self):
        data = await self.request.json()
        message = await self.request.app["db"].message.create(
            text=data['text'],
            created=datetime.now(),
        )
        return web.json_response(
            data={
                'message': {
                    'id': message.id,
                    'text': message.text,
                    'created': str(message.created),
                },
            },
        )