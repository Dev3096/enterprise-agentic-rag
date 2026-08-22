import psycopg

from enterprise_rag.config.settings import get_settings


def get_connection() -> psycopg.Connection:
    settings = get_settings()

    return psycopg.connect(settings.database_url)