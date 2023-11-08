# sheepy
![Overview](/readme_assests/overview.jpg "Overview")

# Requirements
- Python 3.XX
- [Poetry](https://python-poetry.org/)
- Google Account

# Setup
1. Get your API key from [OMDb](https://www.omdbapi.com/)
2. Follow the instructions following **Create a new Google Cloud Project** [here](https://pypi.org/project/EZSheets/) and place your credentials file in the parent folder

3. Create .env file and put in your information (see example.env)
4. The script will automatically create a spreadsheet if no ID was provided.\
    If you already created a spreadsheet you can pass its ID and a sheet will be setup.
5. Run following commands
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
-w, --watched  Set to mark movie as already watched (Defaults to False) 
