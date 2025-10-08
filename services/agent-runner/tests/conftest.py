import os

# Ensure the TESTING environment variable is set before importing the app
os.environ["TESTING"] = "true"

import pytest
import sqlite3
from src.db_init import initialize_database
from fastapi.testclient import TestClient
from src.main import app, set_db_connection

@pytest.fixture(scope="session")
def test_db_connection():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    initialize_database(conn)
    set_db_connection(conn)
    yield conn
    # Let pytest handle the closure of the connection

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch, test_db_connection):
    monkeypatch.setattr("src.main.get_db_connection", lambda: test_db_connection)
    monkeypatch.setenv("REQUIRE_AUTH", "false")
    # ensure set_db_connection is called so app.state.db_conn exists:
    set_db_connection(test_db_connection)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c