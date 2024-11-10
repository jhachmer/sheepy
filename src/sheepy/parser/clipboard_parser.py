import re
import threading
import time
from typing import Callable

import pyperclip


def check_for_imdb_id(clipboard_content: str) -> bool:
    """Checks whether or not arg is a valid imdb id

    Args:
        clipboard_content (str): Current clipboard content

    Returns:
        bool: Returns true if given string is a valid id
    """
    imdb_id_pattern: re.Pattern = re.compile(r"tt\d{7,8}$", re.IGNORECASE)
    match = imdb_id_pattern.match(clipboard_content)
    if match is None:
        return False
    return True


class ClipboardWatcher(threading.Thread):
    """Implements functionality to watch clipboard for content changes
     Pass function to predicate to determine when the callable arg should be triggered
     pause determines the time between polling the clipboard

    Args:
        threading: Inherits from Thread to override run method
    """

    def __init__(
        self,
        predicate: Callable[[str], bool],
        callback: Callable[[str], None],
        pause: float = 5.0,
    ) -> None:
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self) -> None:
        recent_value: str = ""
        while not self._stopping:
            tmp_value: str = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if self._predicate(recent_value):
                    self._callback(recent_value)
            time.sleep(self._pause)

    def stop(self) -> None:
        self._stopping = True
