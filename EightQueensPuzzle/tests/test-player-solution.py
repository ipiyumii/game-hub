import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

# Mock firebase
sys.modules['firebase_admin'] = MagicMock()
sys.modules['firebase_admin.firestore'] = MagicMock()
sys.modules['firebase_admin.credentials'] = MagicMock()

from EightQueensPuzzle.player_solutions import validate_player_solution


class TestValidatePlayerSolution(unittest.TestCase):

    @patch('EightQueensPuzzle.player_solutions.fetch_all_solutions')
    @patch('EightQueensPuzzle.player_solutions.fetch_found_solutions')
    @patch('EightQueensPuzzle.player_solutions.save_found_solution')
    @patch('EightQueensPuzzle.player_solutions.messagebox')
    #find a new answer
    def test_correct_solution_not_found_before(self, mock_messagebox, mock_save, mock_found, mock_all):
        valid_solution = [0, 4, 7, 5, 2, 6, 1, 3]
        mock_all.return_value = [valid_solution, [1, 3, 5, 0, 2, 4, 7, 6]]
        mock_found.return_value = []

        result = validate_player_solution(valid_solution, "piyumi")

        self.assertIn("Congratulations", result)
        self.assertIn("piyumi", result)
        mock_save.assert_called_once_with("piyumi", valid_solution)
    @patch('EightQueensPuzzle.player_solutions.fetch_all_solutions')
    @patch('EightQueensPuzzle.player_solutions.fetch_found_solutions')
    @patch('EightQueensPuzzle.player_solutions.messagebox')
    #find a wrong answer
    def test_incorrect_solution(self, mock_messagebox, mock_found, mock_all):
        invalid_solution = [0, 1, 2, 3, 4, 5, 6, 7]
        mock_all.return_value = [[0, 4, 7, 5, 2, 6, 1, 3], [1, 3, 5, 0, 2, 4, 7, 6]]
        mock_found.return_value = []

        result = validate_player_solution(invalid_solution, "imalka")

        self.assertEqual(result, "Incorrect solution!")
        mock_messagebox.showinfo.assert_called_with("Incorrect", "Incorrect solution!")

    @patch('EightQueensPuzzle.player_solutions.fetch_all_solutions')
    @patch('EightQueensPuzzle.player_solutions.fetch_found_solutions')
    @patch('EightQueensPuzzle.player_solutions.messagebox')
    #already found
    def test_solution_already_found(self, mock_messagebox, mock_found, mock_all):
        solution = [0, 4, 7, 5, 2, 6, 1, 3]
        mock_all.return_value = [solution, [1, 3, 5, 0, 2, 4, 7, 6]]
        mock_found.return_value = [solution]

        result = validate_player_solution(solution, "warna")

        self.assertIn("already found", result)
        mock_messagebox.showinfo.assert_called_with("Info", "This solution was already found by someone else!")


    
# if __name__ == '__main__':
#     unittest.main()