from enterprise_rag.database.connection import get_connection


def test_database_connection():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

    assert result == (1,)

def test_pgvector_is_available():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT '[1,2,3]'::vector;
                """
            )

            result = cursor.fetchone()
            print("Database result:", result)
            print("Result type:", type(result))

    assert result is not None

