import psycopg
from pgvector.psycopg import register_vector

from enterprise_rag.config.settings import get_settings


def get_connection() -> psycopg.Connection:
    settings = get_settings()

    connection = psycopg.connect(settings.database_url)

    register_vector(connection)

    return connection