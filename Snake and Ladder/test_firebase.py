import os
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
import firebase_database as fb
from firebase_database import FirebaseDatabase

# Reset singleton before each test
@pytest.fixture(autouse=True)
def reset_singleton():
    FirebaseDatabase._instance = None
    FirebaseDatabase._initialized = False
    yield


# Test 1: Firebase disabled when credentials file missing
def test_init_without_credentials(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda _: False)

    db = FirebaseDatabase()
    assert db.enabled is False
    assert db.db is None


# Test 2: Firebase initializes correctly
def test_init_success(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    monkeypatch.setattr(fb.credentials, "Certificate", lambda _: object())
    monkeypatch.setattr(fb.firebase_admin, "_apps", {}, raising=False)
    monkeypatch.setattr(fb.firebase_admin, "initialize_app", lambda _: None)

    mock_db = MagicMock()
    monkeypatch.setattr(fb.firestore, "client", lambda: mock_db)
    db = FirebaseDatabase()
    assert db.enabled is True
    assert db.db == mock_db


# Test 3: Save game session
def test_save_game_session():
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    FirebaseDatabase._initialized = True
    db.enabled = True

    mock_db = MagicMock()
    sessions = mock_db.collection.return_value.document.return_value.collection.return_value
    sessions.add.return_value = (None, SimpleNamespace(id="session_1"))

    db.db = mock_db

    session_id = db.save_game_session(
        "Alice", 5, {}, {}, 3, 3, 0.01, 0.02
    )

    assert session_id == "session_1"


# Test 4: Save new player
def test_save_player_details_new_player():
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    FirebaseDatabase._initialized = True
    db.enabled = True

    mock_db = MagicMock()
    players = mock_db.collection.return_value.document.return_value.collection.return_value
    players.where.return_value.limit.return_value.stream.return_value = []
    players.add.return_value = (None, SimpleNamespace(id="player_1"))

    db.db = mock_db
    player_id = db.save_player_details("Bob", 6, 4, "session_1")

    assert player_id == "player_1"


# Test 5: Firebase connection test
def test_test_connection():
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    FirebaseDatabase._initialized = True
    db.enabled = True

    mock_db = MagicMock()
    info_doc = MagicMock()
    info_doc.exists = True

    mock_db.collection.return_value.document.return_value.get.return_value = info_doc
    db.db = mock_db

    assert db.test_connection() is True


# Test 6: is_connected flag
def test_is_connected():
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    FirebaseDatabase._initialized = True

    db.enabled = True
    db.db = object()
    assert db.is_connected() is True

    db.enabled = False
    assert db.is_connected() is False
