import sqlite3
from pathlib import Path
from src.constants import DB_PATH


def get_connection() -> sqlite3.Connection:
    # Path existence check
    if not Path(DB_PATH).is_file():
        raise FileNotFoundError(f"Chinook DB File not found: {DB_PATH}")

    # Connect with row_factory
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Return connection
    return conn
