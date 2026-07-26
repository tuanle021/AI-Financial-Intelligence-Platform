from sqlalchemy import text
from sqlalchemy.engine import Engine


def check_database_connection(
    database_engine: Engine,
) -> bool:
    with database_engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        return result.scalar_one() == 1