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

SHEET_NTH_ROW = 2
SHEET_BACKGROUND_COLOR_EVEN = Color.fromHex("#000000")
SHEET_BACKGROUND_COLOR_ODD = Color.fromHex("#2d2d2d")
SHEET_TEXT_COLOR = Color.fromHex("#FFFFFF")

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
