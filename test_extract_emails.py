import unittest
from unittest.mock import patch, MagicMock
import extract_emails
from utils import store_emails, get_gmail_service

class TestExtractEmails(unittest.TestCase):

    @patch('extract_emails.input', return_value='10')
    @patch('extract_emails.get_gmail_service')
    @patch('extract_emails.store_emails')
    @patch('os.path.exists', return_value=True)
    def test_main_success(self, mock_exists, mock_store_emails, mock_get_gmail_service, mock_input):
        mock_service = MagicMock()
        mock_get_gmail_service.return_value = mock_service

        emails = [{'id': 'msg1'}, {'id': 'msg2'}]
        mock_service.users().messages().list().execute.return_value = {
            'messages': [{'id': 'msg1'}, {'id': 'msg2'}]
        }
        mock_service.users().messages().get().execute.side_effect = emails

        # Call the main function in extract_emails.py
        extract_emails.main()
        
        mock_store_emails.assert_called_once()
        mock_get_gmail_service.assert_called_once()

    @patch('os.path.exists', return_value=False)
    def test_main_file_not_found(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            extract_emails.main()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.input', return_value='invalid')
    def test_main_invalid_email_count(self, mock_exists, mock_input):
        with self.assertRaises(ValueError):
            extract_emails.main()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.input', return_value='-5')
    def test_main_negative_email_count(self, mock_exists, mock_input):
        with self.assertRaises(ValueError):
            extract_emails.main()

if __name__ == '__main__':
    unittest.main()
