# test_firebase.py
import os
from types import SimpleNamespace
from unittest.mock import Mock, MagicMock

import pytest

import firebase_database as fbmod
from firebase_database import FirebaseDatabase


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset singleton before each test so instances don't carry state across tests."""
    fbmod.FirebaseDatabase._instance = None
    fbmod.FirebaseDatabase._initialized = False
    yield
    fbmod.FirebaseDatabase._instance = None
    fbmod.FirebaseDatabase._initialized = False


def test_init_missing_credentials(monkeypatch, tmp_path):
    """If credentials file doesn't exist the instance should be disabled."""
    # Make os.path.exists return False for the expected path
    monkeypatch.setattr(os.path, "exists", lambda p: False)

    db = FirebaseDatabase()
    assert db.enabled is False
    assert db.db is None


def test_init_success_creates_info_doc(monkeypatch):
    """When credentials exist and firestore.client returns a mock, _info doc set should be called."""
    # Make os.path.exists True
    monkeypatch.setattr(os.path, "exists", lambda p: True)

    # Mock credentials.Certificate to prevent reading real file
    monkeypatch.setattr(fbmod.credentials, "Certificate", lambda p: object())

    # Ensure firebase_admin._apps appears empty so initialize_app gets called
    monkeypatch.setattr(fbmod.firebase_admin, "_apps", {}, raising=False)
    init_called = {"value": False}
    def fake_init(app_cred):
        init_called["value"] = True
    monkeypatch.setattr(fbmod.firebase_admin, "initialize_app", fake_init)

    # Create a mock firestore client and its chain (.collection(...).document(...).set)
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_doc = MagicMock()
    # Setup chaining: db.collection('snake_and_ladder').document('_info').set(...)
    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_doc
    mock_doc.set = Mock()

    monkeypatch.setattr(fbmod.firestore, "client", lambda: mock_db)

    # Instantiate
    db = FirebaseDatabase()

    assert db.enabled is True
    assert db.db is mock_db
    # verify the _info doc set was called (collection structure creation)
    mock_collection.document.assert_called_with('_info')
    mock_doc.set.assert_called()
    assert init_called["value"] is True


def test_save_game_session_writes_session(monkeypatch):
    """save_game_session should call add(...) and return the session id."""
    # Prepare instance but bypass init: create instance and set its db to a mock
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    # Reset init flag so we don't run __init__
    FirebaseDatabase._initialized = True
    db.enabled = True

    # Build nested mock for sessions_add
    mock_db = MagicMock()
    sessions_collection = MagicMock()
    sessions_subcollection = MagicMock()

    # chain: db.collection('snake_and_ladder').document('game_sessions').collection('sessions').add(...)
    mock_db.collection.return_value.document.return_value.collection.return_value = sessions_subcollection

    # Simulate add returns (something, reference) where reference.id is session id
    add_return_ref = SimpleNamespace(id="session_123")
    sessions_subcollection.add.return_value = (None, add_return_ref)

    db.db = mock_db

    # call method
    session_id = db.save_game_session(
        player_name="Alice",
        board_size=5,
        snakes={14: 7},
        ladders={3: 22},
        player_choice=4,
        correct_answer=4,
        bfs_time=0.002,
        dijkstra_time=0.001
    )

    assert session_id == "session_123"
    sessions_subcollection.add.assert_called_once()
    # check that stored dict includes expected keys and computed fields
    stored = sessions_subcollection.add.call_args[0][0]
    assert stored["player_name"] == "Alice"
    assert stored["board_size"] == 5
    assert stored["is_correct"] is True
    assert "bfs_time_ms" in stored and "dijkstra_time_ms" in stored


def test_save_player_details_update_and_create(monkeypatch):
    """Test both update existing player and create new player branches."""
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    FirebaseDatabase._initialized = True
    db.enabled = True

    mock_db = MagicMock()
    players_doc_collection = MagicMock()
    players_ref = players_doc_collection  # will act as the returned collection

    # chain: db.collection(...).document('players').collection('player_records')
    mock_db.collection.return_value.document.return_value.collection.return_value = players_ref

    # Case 1: existing_docs found -> update
    existing_doc = MagicMock()
    existing_doc.id = "player_42"

    # 'stream' for existing player returns an iterable with the doc
    players_ref.where.return_value.limit.return_value.stream.return_value = [existing_doc]
    # players_ref.document(...).update should be callable
    players_ref.document.return_value.update = Mock()

    db.db = mock_db

    player_id = db.save_player_details("Bob", board_size=6, correct_answer=5, session_id="sess1")
    assert player_id == "player_42"
    players_ref.document.assert_called_with("player_42")
    players_ref.document.return_value.update.assert_called()

    # Case 2: no existing docs -> create new player
    # Make stream return empty
    players_ref.where.return_value.limit.return_value.stream.return_value = []
    # simulate add returns (None, ref) with id
    players_ref.add.return_value = (None, SimpleNamespace(id="new_player_9"))

    new_id = db.save_player_details("Carol", board_size=6, correct_answer=5, session_id="sess2")
    assert new_id == "new_player_9"
    players_ref.add.assert_called_once()


def test_test_connection_success_and_missing(monkeypatch):
    """test_connection should return True when _info exists, False otherwise."""
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    FirebaseDatabase._initialized = True
    db.enabled = True

    mock_db = MagicMock()
    info_doc = MagicMock()
    info_doc.exists = True
    # chain: db.collection('snake_and_ladder').document('_info').get()
    mock_db.collection.return_value.document.return_value.get.return_value = info_doc
    db.db = mock_db

    assert db.test_connection() is True

    # Now test when exists False
    info_doc.exists = False
    assert db.test_connection() is False


def test_get_player_stats_and_get_all_sessions(monkeypatch):
    """Test retrieval methods return expected values from the mocked DB."""
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    FirebaseDatabase._initialized = True
    db.enabled = True

    mock_db = MagicMock()

    # Mock get_player_stats -> where(...).limit(...).stream() returns docs with to_dict
    player_doc = MagicMock()
    player_doc.to_dict.return_value = {"player_name": "Alice", "total_correct_answers": 2}
    mock_db.collection.return_value.document.return_value.collection.return_value.where.return_value.limit.return_value.stream.return_value = [player_doc]

    # For get_all_sessions -> document('game_sessions').collection('sessions').stream() returns docs
    session_doc = MagicMock()
    session_doc.to_dict.return_value = {"player_name": "Alice", "is_correct": True}
    mock_db.collection.return_value.document.return_value.collection.return_value.stream.return_value = [session_doc]

    db.db = mock_db

    stats = db.get_player_stats("Alice")
    assert isinstance(stats, dict)
    assert stats["player_name"] == "Alice"

    sessions = db.get_all_sessions()
    assert isinstance(sessions, list)
    assert sessions[0]["player_name"] == "Alice"


def test_is_connected_property():
    """is_connected should mirror enabled flag and db presence."""
    db = FirebaseDatabase.__new__(FirebaseDatabase)
    FirebaseDatabase._initialized = True

    db.enabled = True
    db.db = object()
    assert db.is_connected() is True

    db.enabled = False
    assert db.is_connected() is False

