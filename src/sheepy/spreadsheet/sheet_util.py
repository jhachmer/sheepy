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

SHEET_ROW_HEIGHT = 150
SHEET_COL_A_WIDTH = ("A", 70)
SHEET_COL_B_WIDTH = ("B", 300)
SHEET_COL_C_WIDTH = ("C", 40)
SHEET_COL_D_WIDTH = ("D", 300)
SHEET_COL_E_WIDTH = ("F", 60)
SHEET_COL_F_WIDTH = ("E", 100)
SHEET_COL_G_WIDTH = ("G", 80)
SHEET_COL_H_WIDTH = ("H", 92)
SHEET_COL_I_WIDTH = ("I", 150)
SHEET_COL_J_WIDTH = ("J", 300)
SHEET_COL_K_WIDTH = ("K", 150)
