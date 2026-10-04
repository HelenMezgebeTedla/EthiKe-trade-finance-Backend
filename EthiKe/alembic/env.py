import os
import sys

from alembic import context

sys.path.insert(0, os.getcwd())
from database import Base

config = context.config
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    from sqlalchemy import create_engine

    connectable = create_engine(
        os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
