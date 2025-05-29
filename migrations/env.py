from logging.config import fileConfig

"""from sqlalchemy import engine_from_config
from sqlalchemy import pool"""

from alembic import context
#добавила
from sqlalchemy import create_engine

# вместо этого from app.settings import config as app_config
# вот это
#from app.settings import get_config
#app_config = get_config()

from app.store.database.accessor import PostgresAccessor
from app.store.database.models import db

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
#if config.config_file_name is not None:
fileConfig(config.config_file_name)

db_user = os.getenv("DATABASE_USER")
db_password = os.getenv("DATABASE_PASSWORD")
db_host = os.getenv("DATABASE_HOST")
db_name = os.getenv("DATABASE_NAME")

if not all([db_user, db_password, db_host, db_name]):
    raise RuntimeError("Missing one or more required environment variables for DB connection")

database_url = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

config.set_main_option("sqlalchemy.url", database_url)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db # вместо следующей строки
#target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_online():
    # Alembic видит только те модели, которые импортированы в момент генерации миграции.
    # PostgresAccessor инстанцируется и импортит все нужные модели, тем самым позволяя автогенерировать миграции
    print("App config loaded:", app_config)
    print("Database URL:", app_config["postgres"]["database_url"])
    PostgresAccessor()
    connectable = create_engine(app_config["postgres"]["database_url"])
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
"""def run_migrations_offline() -> None:
    ###Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    ###
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    ###Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    ###
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()"""
