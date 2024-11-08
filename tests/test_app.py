import pytest
import pandas as pd
import sqlite3
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the modules to test
import data_gatherer.api as api
import transformer.transformer as transformer
import database.database as database

# Test fetching data from the API
def test_fetch_data_engineer_jobs():
    # Test that data is fetched successfully and is not empty
    data = api.fetch_data_engineer_jobs()
    assert isinstance(data, list), "Data fetched should be a list"
    assert len(data) > 0, "Data list should not be empty"

# Test transforming the data into a pandas DataFrame
def test_transform_data():
    # Provide sample raw data for testing
    sample_data = [{
        "headline": "Data Engineer",
        "employer": {"name": "Tech Corp"},
        "workplace_address": {"municipality": "Stockholm"},
        "application_deadline": "2024-12-31T23:59:59",
        "webpage_url": "https://example.com",
        "description": {"text": "Job description here"}
    }]

    # Transform the sample data
    df = transformer.transform_data(sample_data)
    assert isinstance(df, pd.DataFrame), "Transformed data should be a DataFrame"
    assert len(df) == 1, "DataFrame should have one row"
    assert list(df.columns) == ["title", "company", "location", "application deadline", "webpage", "description"], "DataFrame should have the correct columns"

# Test exporting data to SQLite
def test_export_to_sqlite():
    # Create a sample DataFrame for testing
    df = pd.DataFrame([{
        "title": "Data Engineer",
        "company": "Tech Corp",
        "location": "Stockholm",
        "application deadline": "2024-12-31",
        "webpage": "https://example.com",
        "description": "Job description here"
    }])

    # Export to a test SQLite database
    db_filename = "test_data_engineer_jobs.db"
    database.export_to_sqlite(df, db_filename)

    # Check if the database file was created
    assert os.path.exists(db_filename), "Database file should be created"

    # Check the contents of the database
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data_engineer_jobs")
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) == 1, "Database should contain one row of data"

    # Clean up the test database file
    os.remove(db_filename)
