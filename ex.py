import urllib

import gspread

from sheepy.omdbapi.omdb import get_movie_data

print(get_movie_data("tt17351924"))
print(urllib.parse.quote("/El Niño/"))


gc = gspread.service_account()

sh = gc.open("Kopie von Movie List (Jannes & Felix)")

print(sh.sheet1.get("A1"))
