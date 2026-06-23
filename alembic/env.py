# alembic/env.py
import sys
import os
# Forzamos a Python a agregar la raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# --- IMPORTACIÓN DE TUS MODELOS ---
from app.database.connection import Base
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

# Objeto de configuración de Alembic (lee el alembic.ini)
config = context.config

# Configuración de Logs del sistema
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Le pasamos los metadatos de tus clases de Python a Alembic para el autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True  # Evita errores de alteración de tablas en SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo online (Conectado a la BD)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            render_as_batch=True  # Súper clave para soportar llaves foráneas en SQLite
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()