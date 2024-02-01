from sheepy_cli.omdb import get_movie_data
import urllib

print(get_movie_data("tt17351924"))
print(urllib.parse.quote('/El Niño/'))