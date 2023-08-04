import unittest
from unittest.mock import patch, mock_open
from project import Weight

class TestWeight(unittest.TestCase):

    # Test if the log_weight function is working properly
    @patch("builtins.input", side_effect=[70])
    @patch("builtins.open", new_callable=mock_open)
    def test_log_weight(self, mock_file, mock_input):
        weight = Weight("test_log.csv")
        weight.log_weight()
        mock_file.assert_called_once_with("test_log.csv", "a")
        mock_file().write.assert_called_once()

    # Test if the set_goal function is working properly
    @patch("builtins.input", side_effect=[70])
    @patch("builtins.open", new_callable=mock_open)
    def test_set_goal(self, mock_file, mock_input):
        weight = Weight("test_log.txt")
        weight.set_goal()
        mock_file.assert_called_once_with("test_log.txt", "w")
        mock_file().write.assert_called_once()

    # Test if the view_goal function is working properly
    @patch("builtins.open", new_callable=mock_open, read_data="70")
    def test_view_goal(self, mock_file):
        weight = Weight("test_log.csv")
        weight.view_goal()
        mock_file.assert_any_call("test_log.csv", "r")
        mock_file().read.assert_called_once()

if __name__ == "__main__":
    unittest.main()