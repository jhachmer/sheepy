"""Utility Constants"""
from gspread_formatting import Color

COLUMNS = [
    "Watched?",
    "Title",
    "Year",
    "Genre",
    "Runtime",
    "Suggested by",
    "IMDb Score",
    "Tomatometer",
    "Director",
    "Plot",
    "Movie Poster",
]

SHEET_COLUMNS_RANGE = "A:K"
SHEET_HEADER_RANGE = "A1:K1"

SHEET_BACKGROUND_COLOR = Color(0, 0, 0)
SHEET_TEXT_COLOR = Color(1, 1, 1)
