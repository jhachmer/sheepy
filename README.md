# sheepy
![Overview](/readme_assests/overview.png "Overview")

# Requirements
- Python 3.12 (older versions may also work)
- Google Account

# Setup
1. Get your API key from [OMDb](https://www.omdbapi.com/)
2. Follow the instructions under **Enable API Access for a Project** and **For Bots: Using Service Account** [here](https://docs.gspread.org/en/latest/oauth2.html) to set up Google API access
3. Create .env file and put in your information (see example.env)
4. Run following commands
    ```sh
    # make sure you are in the projects root folder
    # install dependencies
    pip install .
    # to install dev dependencies
    pip install .[dev] 
    # run program
    # (see below for more options)
    python -m sheepy -h
    ```

# Usage

### Logging
Change logging level by passing a `LOG_LEVEL` environment variable

### General
```sh
usage: sheepy \[-h] {new,view,add} ...

Add or view movies to your personal database.

options:
  -h, --help      show this help message and exit

subcommands:
  {new,view,add}  Commands offered by sheepy
    new           Create a new sheet
    view          View Movie Info
    add           Add Movie to Sheet
```
### Adding
```sh
usage: sheepy add \[-h] \[-w] imdb_id

positional arguments:
  imdb_id        Enter the movies imdb id to add.

options:
  -h, --help     show this help message and exit
  -w, --watched  Set to mark movie as already watched (Defaults to False)
```
### Viewing
```sh
usage: sheepy view [-h] imdb_id

positional arguments:
  imdb_id     Enter the movies imdb id to view.

options:
  -h, --help  show this help message and exit
```
### Creating new sheet
```sh
usage: sheepy new [-h] email

positional arguments:
  email       Enter E-Mail Address of Google Account.

options:
  -h, --help  show this help message and exit
```