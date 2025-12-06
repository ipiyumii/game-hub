from unittest.mock import patch, MagicMock

import pytest

from EightQueensPuzzle.eightqueen_dbUtil import (save_sequencial_solutions_eigh_queens,save_threaded_solutions_eight_queens)

@pytest.fixture
def mock_firestore():
    with patch("EightQueensPuzzle.eightqueen_dbUtil.firestore") as mock_fs:
        mock_client = MagicMock()
        mock_fs.client.return_value = mock_client
        mock_collection = MagicMock()
        mock_client.collection.return_value.document.return_value.collection.return_value = mock_collection
        yield mock_collection

def test_save_sequential_calls_firestore(mock_firestore):
    solutions = [[0,1,2,3,4,5,6,7]]  # dummy solution
    save_sequencial_solutions_eigh_queens(solutions, N=8)

    #  call add for each solution
    assert mock_firestore.add.call_count == len(solutions)

def test_save_threaded_calls_firestore(mock_firestore):
    solutions = [[7,6,5,4,3,2,1,0]]
    save_threaded_solutions_eight_queens(solutions, N=8)

    assert mock_firestore.add.call_count == len(solutions)