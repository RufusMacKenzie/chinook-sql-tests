# Chinook SQL pytest Test Suite

A pytest-based test suite validating the Chinook sample database using SQLite, 
built as a portfolio project to demonstrate SQL query testing practices.

## About Chinook
The Chinook database is a sample music store database with 11 tables covering 
artists, albums, tracks, customers, invoices, employees, and playlists. 
More info at [github.com/lerocha/chinook-database](https://github.com/lerocha/chinook-database).

## What's tested

### Schema validation
- All 11 expected tables exist
- Row counts match expected values for all tables
- Key columns exist with correct data types on selected tables

### JOIN queries
- All albums have associated artists (2-table INNER JOIN)
- All tracks have albums and artists (3-table INNER JOIN)
- Employee/manager relationships (self-JOIN, LEFT and INNER)
- Known employee reports to correct manager

### Aggregations
- Top artist by track count (Iron Maiden — 213 tracks)
- Track count by genre
- Invoice count by country (USA leads with 91)
- Total sales by country
- Average track length within expected range
- Known customer invoice count

## Tech Stack
- Python / pytest
- pytest-check for soft assertions
- SQLite (built-in)
- GitHub Actions CI/CD

## Running the tests
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `pytest`
