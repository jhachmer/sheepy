from sheepy.omdbapi.omdb import extract_movie_data, get_movie_data
from sheepy.spreadsheet.spreadsheet import SheepySpreadsheet

movie_dict = get_movie_data("tt17351924")
extracted_data = extract_movie_data(movie_data=movie_dict, add=True, watched=True)
# print(urllib.parse.quote("/El Niño/"))
env_spreadsheet: SheepySpreadsheet = SheepySpreadsheet.from_env_file()
# new_spreadsheet: SheepySpreadsheet = SheepySpreadsheet.from_new()
# env_spreadsheet.transfer_ownership("jannes.hachmer@gmail.com")
# env_spreadsheet.spreadsheet.accept_ownership("03575909994618432849")

env_spreadsheet.add_movie_to_sheet(extracted_data)

# print(env_spreadsheet.find_free_row())
