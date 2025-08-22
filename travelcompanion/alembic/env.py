import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from travelcompanion.config import DATABASE_URL
from travelcompanion.models.database import db_helper
from travelcompanion.models.base import Base
from travelcompanion.models.testtable import TestTable
target_metadata = Base.metadata

# Alembic config object
config = context.config

# Динамически подставляем URL из config.py
config.set_main_option("sqlalchemy.url", DATABASE_URL)

fileConfig(config.config_file_name)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode using async engine."""
    async with db_helper.engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
