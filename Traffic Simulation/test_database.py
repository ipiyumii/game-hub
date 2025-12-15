import unittest
from unittest.mock import Mock, patch
from firebase_handler import FirebaseHandler
from validation import Validation


class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        self.firebase = FirebaseHandler()
        self.firebase.db = Mock()  # Mock the database

    def test_validate_player_name(self):
        """Test player name validation"""
        # Valid names
        self.assertTrue(Validation.validate_player_name("John")[0])
        self.assertTrue(Validation.validate_player_name("Alice Smith")[0])
        self.assertTrue(Validation.validate_player_name("Player123")[0])

        # Invalid names
        self.assertFalse(Validation.validate_player_name("")[0])
        self.assertFalse(Validation.validate_player_name("A")[0])
        self.assertFalse(Validation.validate_player_name("ThisNameIsWayTooLongForTheGame")[0])

    def test_validate_flow_answer(self):
        """Test flow answer validation"""
        # Valid answers
        self.assertTrue(Validation.validate_flow_answer("15")[0])
        self.assertTrue(Validation.validate_flow_answer("0")[0])
        self.assertTrue(Validation.validate_flow_answer("25")[0])

        # Invalid answers
        self.assertFalse(Validation.validate_flow_answer("-5")[0])
        self.assertFalse(Validation.validate_flow_answer("150")[0])
        self.assertFalse(Validation.validate_flow_answer("abc")[0])
        self.assertFalse(Validation.validate_flow_answer("")[0])

    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.credentials.Certificate')
    def test_firebase_initialization(self, mock_cred, mock_init):
        """Test Firebase initialization"""
        mock_cred.return_value = Mock()
        mock_init.return_value = Mock()

        success = self.firebase.initialize_firebase()
        self.assertTrue(success)
        self.assertTrue(self.firebase.initialized)

if __name__ == '__main__':
    unittest.main()