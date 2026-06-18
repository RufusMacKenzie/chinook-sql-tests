import pytest

from src.db import get_connection


@pytest.fixture(scope="session")
def db_connection():
    conn = get_connection()
    yield conn
    conn.close()
