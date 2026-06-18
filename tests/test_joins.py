import pytest_check as check


def test_all_albums_have_artists(db_connection):
    # JOIN Album to Artist, verify no NULLs in artist name, verify count matches Album row count (347)
    cursor = db_connection.cursor()
    rows = cursor.execute(
        "SELECT a.Title, ar.Name FROM Album a INNER JOIN Artist ar ON a.ArtistId = ar.ArtistId;"
    ).fetchall()
    check.equal(347, len(rows), f"Expected 347 album records; got {len(rows)}")
    for row in rows:
        check.is_not_none(row["Name"], f"Null artist name for album {row['Title']}")


def test_all_tracks_have_albums_and_artists(db_connection):
    # 3-table JOIN, verify count matches Track row count (3503), no NULLs
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT t.Name as TrackName, a.Title as AlbumTitle, ar.Name as ArtistName
        FROM Track t
        INNER JOIN Album a ON t.AlbumId = a.AlbumId
        INNER JOIN Artist ar ON a.ArtistId = ar.ArtistId;
        """).fetchall()
    check.equal(3503, len(rows), f"Expected 3503 Track records; got {len(rows)}")
    for row in rows:
        check.is_not_none(
            row["AlbumTitle"], f"Null AlbumTitle for Track {row['TrackName']}"
        )
        check.is_not_none(
            row["ArtistName"], f"Null ArtistName for Track {row['TrackName']}"
        )


def test_employee_manager_left_join(db_connection):
    # LEFT JOIN Employee to itself, verify 8 rows total
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT e.FirstName, e.LastName, m.FirstName, m.LastName 
        FROM Employee e 
        LEFT JOIN Employee m ON e.ReportsTo = m.EmployeeId;
    """).fetchall()
    assert len(rows) == 8


def test_employee_manager_inner_join(db_connection):
    # INNER JOIN Employee to itself, verify 7 rows (Andrew excluded)
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT e.FirstName, e.LastName, m.FirstName, m.LastName 
        FROM Employee e 
        INNER JOIN Employee m ON e.ReportsTo = m.EmployeeId;
    """).fetchall()
    assert len(rows) == 7


def test_known_employee_manager(db_connection):
    # verify Nancy Edwards reports to Andrew Adams specifically
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT e.FirstName as EmployeeFirstName, e.LastName as EmployeeLastName, 
        m.FirstName as ManagerFirstName, m.LastName as ManagerLastName 
        FROM Employee e 
        INNER JOIN Employee m ON e.ReportsTo = m.EmployeeId
        WHERE e.FirstName = 'Nancy' AND e.LastName = 'Edwards';
    """).fetchall()
    check.equal(1, len(rows), "Duplicate Employee found: Nancy Edwards")
    check.equal(rows[0]["ManagerFirstName"], "Andrew")
    check.equal(rows[0]["ManagerLastName"], "Adams")
