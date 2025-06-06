from aiohttp import web  # основной модуль aiohttp
import jinja2  # шаблонизатор jinja2
import aiohttp_jinja2  # адаптация jinja2 к aiohttp

from app.settings import config, BASE_DIR
from app.forum.routes import setup_routes as setup_forum_routes
from app.store.database.accessor import PostgresAccessor

def setup_config(application):
    application["config"] = config
    
def setup_accessors(application):
    application['db'] = PostgresAccessor()
    application['db'].setup(application)

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
   setup_forum_routes(application)  # настраиваем url-пути приложения forum



def setup_app(application):
   setup_config(application)# добавилось после подключения конфига
   setup_accessors(application)# добавили подключение аксессора
   # настройка всего приложения состоит из:
   setup_external_libraries(application)  # настройки внешних библиотек, например шаблонизатора
   setup_routes(application)  # настройки роутера приложения

app = web.Application()  # создаем наш веб-сервер

if __name__ == "__main__":  # эта строчка указывает, что данный файл можно запустить как скрипт
   setup_app(app)  # настраиваем приложение
   web.run_app(app, port=config["common"]["port"])# вместо следующей строки "до появления конфига"
   #web.run_app(app)  # запускаем приложение