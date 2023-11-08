# sheepy
![Overview](/readme_assests/overview.jpg "Overview")

# Requirements
- Python 3.XX
- [Poetry](https://python-poetry.org/)
- Google Account

# Setup
1. Get your API key from [OMDb](https://www.omdbapi.com/)
2. TODO: Google API Setup
3. Create .env file and put in your information (see example.env)
4. Run following commands
    ```sh
    # make sure you are in the projects parent dir
    # install dependencies
    poetry install
    # run program
    poetry run python .\sheepy\core.py [-h] (-a | -v) [-w] imdb_id
    # see below for more detail
    ```

# Usage
usage: core.py [-h] (-a | -v) [-w] imdb_id

Add or view movies to your personal database.

positional arguments:\
  imdb_id        Enter the movies imdb id.

options:\
-h, --help     show this help message and exit\
-a, --add      Set to add to sheet (This or -v/--view is required)\
-v, --view     Set to view in the CLI (This or -a/--add is required) \
-w, --watched  Set to mark movie as already watched (Defaults to False) \