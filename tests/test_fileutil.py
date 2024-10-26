import os

from sheepy.util import file


class TestFileUtil:
    def test_delete_csv(self, mocker):
        """
        Test the removal of a file using mocking to avoid actual file system operations.
        """
        filename = "temp_file.csv"
        mock_remove = mocker.patch("os.remove")
        mocker.patch("os.path.isfile", return_value=False)
        mocker.patch("builtins.open", mocker.mock_open())
        file.delete_csv("temp_file.csv")
        mock_remove.assert_called_once_with(filename)
        assert not os.path.isfile(filename)
