import pytest_check as check


def test_top_artist_by_track_count(db_connection):
    # the artist with the most tracks should be a specific known artist. Look it up in DB Browser first.
    EXPECTED_IRON_MAIDEN_TRACKS = 213
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT ar.Name, COUNT(t.TrackId) as TrackCount
        FROM Artist ar
        INNER JOIN Album a ON ar.ArtistId = a.ArtistId
        INNER JOIN Track t ON a.AlbumId = t.AlbumId
        GROUP BY ar.Name
        ORDER BY TrackCount DESC
        LIMIT 1;
    """).fetchall()

    check.equal(1, len(rows), f"Expected 1 top artist but got {len(rows)}")
    check.equal(
        "Iron Maiden",
        rows[0]["Name"],
        f"Expected Artist 'Iron Maiden'; got  {rows[0]['Name']}",
    )
    check.equal(
        EXPECTED_IRON_MAIDEN_TRACKS,
        rows[0]["TrackCount"],
        f"Expected {EXPECTED_IRON_MAIDEN_TRACKS} tracks; got {rows[0]['TrackCount']}",
    )


def test_track_count_by_genre(db_connection):
    # verify a specific genre has an expected number of tracks
    EXPECTED_METAL_TRACKS = 374
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT g.Name as GenreName, COUNT(t.TrackId) as TrackCount
        FROM Genre g
        INNER JOIN Track t ON t.GenreId = g.GenreId
        WHERE g.Name = 'Metal';
    """).fetchall()

    check.equal(1, len(rows), f"Expected 1 matching genre name but got {len(rows)}")
    check.equal(
        "Metal",
        rows[0]["GenreName"],
        f"Expected Genre 'Metal'; got  {rows[0]['GenreName']}",
    )
    check.equal(
        EXPECTED_METAL_TRACKS,
        rows[0]["TrackCount"],
        f"Expected {EXPECTED_METAL_TRACKS} Metal tracks; got {rows[0]['TrackCount']}",
    )


def test_genres_with_more_than_100_tracks(db_connection):
    EXPECTED_GENRE_COUNT = 5
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT g.Name, COUNT(t.TrackId) as TrackCount
        FROM Genre g
        INNER JOIN Track t ON t.GenreId = g.GenreId
        GROUP BY g.Name
        HAVING COUNT(t.TrackId) > 100
        ORDER BY TrackCount DESC
    """).fetchall()

    check.equal(
        EXPECTED_GENRE_COUNT,
        len(rows),
        f"Expected {EXPECTED_GENRE_COUNT} genres with >100 tracks, got {len(rows)}",
    )
    check.equal("Rock", rows[0]["Name"], "Expected Rock to be top genre")
    check.equal(1297, rows[0]["TrackCount"], "Expected Rock to have 1297 tracks")


def test_tracks_longer_than_average(db_connection):
    EXPECTED_COUNT = 494
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT Name, Milliseconds
        FROM Track
        WHERE Milliseconds > (SELECT AVG(Milliseconds) FROM Track)
        ORDER BY Milliseconds DESC
    """).fetchall()

    check.equal(
        EXPECTED_COUNT,
        len(rows),
        f"Expected {EXPECTED_COUNT} tracks longer than average, got {len(rows)}",
    )
    # First row should be the longest track
    check.is_true(
        rows[0]["Milliseconds"] > rows[-1]["Milliseconds"],
        "Results should be ordered longest first",
    )


def test_total_invoices_by_country(db_connection):
    # count of Invoices grouped by country, verify USA is the top country
    EXPECTED_TOP_INVOICE_COUNTRY = "USA"
    EXPECTED_TOP_INVOICE_COUNT = 91
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT BillingCountry, COUNT(InvoiceId) as InvoiceCount
        FROM Invoice
        GROUP BY BillingCountry
        ORDER BY InvoiceCount DESC
        LIMIT 1;
    """).fetchall()

    check.equal(
        1, len(rows), f"Expected 1 matching top invoice country but got {len(rows)}"
    )
    check.equal(
        EXPECTED_TOP_INVOICE_COUNTRY,
        rows[0]["BillingCountry"],
        f"Expected Billing Country '{EXPECTED_TOP_INVOICE_COUNTRY}'; got  {rows[0]['BillingCountry']}",
    )
    check.equal(
        EXPECTED_TOP_INVOICE_COUNT,
        rows[0]["InvoiceCount"],
        f"Expected {EXPECTED_TOP_INVOICE_COUNT} Invoices; got {rows[0]['InvoiceCount']}",
    )


def test_total_sales_by_country(db_connection):
    # sum of Invoice totals grouped by country, verify USA is the top country
    EXPECTED_TOP_INVOICE_TOTAL_COUNTRY = "USA"
    EXPECTED_TOP_INVOICE_TOTAL = 523.06
    cursor = db_connection.cursor()
    rows = cursor.execute("""
        SELECT BillingCountry, ROUND(SUM(Total),2) as InvoiceTotal
        FROM Invoice
        GROUP BY BillingCountry
        ORDER BY InvoiceTotal DESC
        LIMIT 1;
    """).fetchall()

    check.equal(
        1,
        len(rows),
        f"Expected 1 matching top invoice total country but got {len(rows)}",
    )
    check.equal(
        EXPECTED_TOP_INVOICE_TOTAL_COUNTRY,
        rows[0]["BillingCountry"],
        f"Expected Billing Country '{EXPECTED_TOP_INVOICE_TOTAL_COUNTRY}'; got  {rows[0]['BillingCountry']}",
    )
    check.equal(
        EXPECTED_TOP_INVOICE_TOTAL,
        rows[0]["InvoiceTotal"],
        f"Expected {EXPECTED_TOP_INVOICE_TOTAL} Invoices; got {rows[0]['InvoiceTotal']}",
    )


def test_average_track_length(db_connection):
    # average Milliseconds across all tracks, verify it's within a reasonable range
    MIN_EXPECTED_AVERAGE = 393500.0
    MAX_EXPECTED_AVERAGE = 393700.0
    cursor = db_connection.cursor()
    rows = cursor.execute("SELECT AVG(Milliseconds) as Average FROM Track;").fetchall()

    check.equal(1, len(rows), f"Expected 1 average but got {len(rows)}")
    actual_average = rows[0]["Average"]
    check.between(
        actual_average,
        MIN_EXPECTED_AVERAGE,
        MAX_EXPECTED_AVERAGE,
        f"Average Track Length expected between {MIN_EXPECTED_AVERAGE} and {MAX_EXPECTED_AVERAGE} but was {actual_average}",
    )


def test_customer_invoice_count(db_connection):
    # verify a known customer has a specific number of invoices
    EXPECTED_CUSTOMER_NAME = "Puja Srivastava"
    EXPECTED_CUSTOMER_ID = 59
    EXPECTED_INVOICE_COUNT = 6
    cursor = db_connection.cursor()
    rows = cursor.execute(
        """
        SELECT c.FirstName || ' ' || c.LastName as CustomerName, c.CustomerId, COUNT(i.InvoiceId) as InvoiceCount
        FROM Customer c
        INNER JOIN Invoice i ON c.CustomerId = i.CustomerId
        WHERE c.CustomerId = ?
        GROUP BY c.CustomerId;
    """,
        (EXPECTED_CUSTOMER_ID,),
    ).fetchall()

    check.equal(1, len(rows), f"Expected 1 record but got {len(rows)}")
    customer_name = rows[0]["CustomerName"]
    check.equal(
        EXPECTED_CUSTOMER_NAME,
        customer_name,
        f"Expected CustomerName = {EXPECTED_CUSTOMER_NAME} but got {customer_name}",
    )
    invoice_count = rows[0]["InvoiceCount"]
    check.equal(
        EXPECTED_INVOICE_COUNT,
        invoice_count,
        f"Expected {EXPECTED_INVOICE_COUNT} invoices, but got {invoice_count}",
    )
