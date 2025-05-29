from aiohttp import web  # основной модуль aiohttp
import jinja2  # шаблонизатор jinja2
import aiohttp_jinja2  # адаптация jinja2 к aiohttp

from app.settings import config, BASE_DIR
from config.config_loader import load_config
from app.store.database.accessor import PostgresAccessor
from app.forum.routes import setup_routes as setup_forum_routes

def setup_config(application):
    config=load_config()
    application["config"] = config
    
#def setup_accessors(application):
    #application['db'] = PostgresAccessor()
    #application['db'].setup(application)

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



async def setup_app(application):
   setup_config(application)# добавилось после подключения конфига
   setup_external_libraries(application)  # настройки внешних библиотек, например шаблонизатора
   #setup_accessors(application)# добавили подключение аксессора
   await application['db'].setup(application)
   setup_routes(application)  # настройки роутера приложения


if __name__ == "__main__":  # эта строчка указывает, что данный файл можно запустить как скрипт
   import asyncio
   
   async def main():
    app = web.Application()  # создаем наш веб-сервер 
    application['db'] = PostgresAccessor()
    
    await setup_app(app)  # настраиваем приложение
    web.run_app(app, port=config["common"]["port"])# вместо следующей строки "до появления конфига"
    
    asyncio.run(main())