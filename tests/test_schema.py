import pytest_check as check

EXPECTED_TABLES = {
    "Album",
    "Artist",
    "Customer",
    "Employee",
    "Genre",
    "Invoice",
    "InvoiceLine",
    "MediaType",
    "Playlist",
    "PlaylistTrack",
    "Track",
}

EXPECTED_ROW_COUNTS = {
    "Artist": 275,
    "Album": 347,
    "Track": 3503,
    "Customer": 59,
    "Employee": 8,
    "Genre": 25,
    "Invoice": 412,
    "InvoiceLine": 2240,
    "MediaType": 5,
    "Playlist": 18,
    "PlaylistTrack": 8715,
}

EXPECTED_COLUMNS = {
    "Artist": {
        "ArtistId": "INTEGER",
        "Name": "NVARCHAR(120)",
    },
    "Track": {
        "TrackId": "INTEGER",
        "Name": "NVARCHAR(200)",
        "AlbumId": "INTEGER",
        "MediaTypeId": "INTEGER",
        "GenreId": "INTEGER",
        "Milliseconds": "INTEGER",
        "UnitPrice": "NUMERIC(10,2)",
    },
    "Invoice": {
        "InvoiceId": "INTEGER",
        "CustomerId": "INTEGER",
        "InvoiceDate": "DATETIME",
        "Total": "NUMERIC(10,2)",
    },
    "Employee": {
        "EmployeeId": "INTEGER",
        "LastName": "NVARCHAR(20)",
        "ReportsTo": "INTEGER",  # self-join column — worth explicitly testing
    },
}


def test_expected_tables_exist(db_connection):
    cursor = db_connection.cursor()
    tables = {
        row["name"]
        for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    }
    assert tables == EXPECTED_TABLES


def test_expected_row_counts(db_connection):
    cursor = db_connection.cursor()
    for table_name in EXPECTED_TABLES:
        expected_count = EXPECTED_ROW_COUNTS.get(table_name)
        if expected_count is None:
            continue  # no count to verify for this table
        actual_count = cursor.execute(
            f"SELECT COUNT(*) FROM {table_name};"  # safe - table_name from EXPECTED_TABLES whitelist
        ).fetchone()[0]
        check.equal(
            expected_count,
            actual_count,
            f"Row count for table {table_name}: expected {expected_count}, got {actual_count}",
        )


def test_expected_columns(db_connection):
    cursor = db_connection.cursor()
    for table_name in EXPECTED_COLUMNS.keys():
        actual_columns = {
            row["name"]: row["type"]
            for row in cursor.execute(
                f"PRAGMA table_info({table_name});"
            )  # safe - table_name from EXPECTED_COLUMNS whitelist
        }
        expected_columns = EXPECTED_COLUMNS.get(table_name)
        for column_to_check in expected_columns.keys():
            if check.is_true(
                column_to_check in actual_columns,
                f"Table {table_name}: Missing column {column_to_check}",
            ):
                expected_type = expected_columns.get(column_to_check)
                check.equal(
                    actual_columns[column_to_check],
                    expected_type,
                    f"Table {table_name}: Type mismatch for {column_to_check}",
                )
