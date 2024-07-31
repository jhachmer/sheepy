"""Utilities to manipulate strings"""


def insert_newlines(string: str, nth: int = 64) -> str:
    """inserts newlines at every nth character

    Args:
        string (str): string to alter
        every (int, optional): number of occurences when newline is inserted.
         Defaults to 64.

    Returns:
        str: returns new string with newlines
    """
    lines = []
    for i in range(0, len(string), nth):
        lines.append(string[i : i + nth])
    return "\n".join(lines)
