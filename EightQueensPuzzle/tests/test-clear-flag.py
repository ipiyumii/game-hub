import unittest
from unittest.mock import MagicMock, patch
from EightQueensPuzzle.player_solutions import clear_found_solutions

class TestClearFlag(unittest.TestCase):

    @patch("EightQueensPuzzle.player_solutions.firestore")
    @patch("EightQueensPuzzle.player_solutions.delete_collection")
    def test_clear_found_solutions_logic(self, mock_delete, mock_firestore):

        # Fake firebase
        mock_db = MagicMock()
        mock_firestore.client.return_value = mock_db

        mock_collection = MagicMock()
        mock_db.collection.return_value.document.return_value.collection.return_value = (
            mock_collection
        )

    #fucntion call
        clear_found_solutions()

        # test path
        mock_db.collection.assert_called_once_with("eightqueens")
        mock_db.collection.return_value.document.assert_called_once_with(
            "player_solutions"
        )
        mock_db.collection.return_value.document.return_value.collection.assert_called_once_with(
            "N8"
        )

        # test delete collection
        mock_delete.assert_called_once_with(mock_collection)

# if __name__ == "__main__":
#     unittest.main()
