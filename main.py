from aiohttp import web  # основной модуль aiohttp
import jinja2  # шаблонизатор jinja2
import aiohttp_jinja2  # адаптация jinja2 к aiohttp

from app.settings import get_config, BASE_DIR
from app.store.database.accessor import PostgresAccessor
from app.forum.routes import setup_routes as setup_forum_routes

def setup_config(application):
    #application["config"] = get_config()
    try:
        config = get_config()
        application["config"] = config
    except RuntimeError as e:
        print(f"Failed to load configuration: {e}")
        raise
    
#def setup_accessors(application):
    #application['db'] = PostgresAccessor()
    #application['db'].setup(application)
    
async def on_startup(app):
    await app['db'].setup(app)

def setup_accessors(application):
    application['db'] = PostgresAccessor()
    application.on_startup.append(on_startup)

#вместо первоначального варианта!
def setup_external_libraries(application):
    aiohttp_jinja2.setup(
        application,
        loader=jinja2.FileSystemLoader(f"{BASE_DIR}/templates"),
    )
    
#def setup_external_libraries(application: web.Application) -> None:
   # указываем шаблонизатору, что html-шаблоны надо искать в папке templates
   #aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader("templates"))

# в этой функции производится настройка url-путей для всего приложения
def setup_routes(application):
   # здесь был импорт сетап_роутс
    setup_forum_routes(application)  # настраиваем url-пути приложения forum
   
    static_dir = {BASE_DIR} / "static"
    application.router.add_static("/static/", path=static_dir, name="static")

def setup_app(application):
   setup_config(application)# добавилось после подключения конфига
   setup_external_libraries(application)  # настройки внешних библиотек, например шаблонизатора
   setup_accessors(application)# добавили подключение аксессора
#   await application['db'].setup(application)
   setup_routes(application)  # настройки роутера приложения

app = web.Application()
setup_app(app)
if __name__ == "__main__":  # эта строчка указывает, что данный файл можно запустить как скрипт
#   import asyncio
   
#   async def main():
# создаем наш веб-сервер 
#       application['db'] = PostgresAccessor()
    
#       await 
  # настраиваем приложение
    web.run_app(app, port=app["config"]["common"]["port"])# вместо следующей строки "до появления конфига"
    
#    asyncio.run(main())