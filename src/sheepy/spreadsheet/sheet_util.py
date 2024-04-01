"""Utility Constants for row, column colors, widths and heights etc."""

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

SHEET_BACKGROUND_COLOR_EVEN = Color(0, 0, 0)
SHEET_BACKGROUND_COLOR_ODD = Color(0.5, 0.5, 0.5)
SHEET_TEXT_COLOR = Color(1, 1, 1)

SHEET_ROW_HEIGHT = 150
COLUMN_WIDTHS = [
    ("A", 70),
    ("B", 300),
    ("C", 40),
    ("D", 300),
    ("E", 60),
    ("F", 100),
    ("G", 80),
    ("H", 92),
    ("I", 150),
    ("J", 300),
    ("K", 150),
]
SHEET_PLOT_COL = "J"
