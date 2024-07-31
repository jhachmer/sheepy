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


def build_request_url(
    base_url: str, api_key: str, title_or_id: str, year: int | None = None
) -> str:
    """builds requests url for omdb api
     if year is provieded an url is build based on title and year
     otherwise url is build using imdb id

    Args:
        base_url (str): base url for request (https://xyz.com)
        api_key (str): key for api access
        title_or_id (str): title or id identifying movie
        year (int | None, optional): year in which movie was released. Defaults to None.

    Returns:
        str: returns build url for api request
    """
    if year is not None:
        return base_url + api_key + "&t=" + title_or_id + "&y=" + str(year)
    return base_url + api_key + "&i=" + title_or_id
