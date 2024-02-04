"""Spreadsheet Module"""

from typing import Self

import gspread


class Spreadsheet:
    """_summary_"""

    def __init__(self) -> None:
        try:
            self.client: gspread.client.Client = gspread.service_account()
        except FileNotFoundError as fnfe:
            raise SystemExit(
                f"Unable to create service account. Check credentials file. {str(fnfe)}"
            ) from fnfe
        self.sheet: gspread.spreadsheet.Spreadsheet | None = None

    @classmethod
    def from_name(cls, name: str) -> Self:
        """Instantiate Spreadsheet with name of spreadsheet.

        Args:
            name (str): Name of Spreadsheet

        Raises:
            SystemExit: Raises Exception if no spreadsheet with name could be found.

        Returns:
            Self: Returns Spreadsheet instance
        """
        sh = cls()
        try:
            sh.sheet = sh.client.open(name)
        except gspread.exceptions.SpreadsheetNotFound as snf:
            raise SystemExit(
                f"Could not find spreadsheet with name {name}. {str(snf)}"
            ) from snf

        return sh

    @classmethod
    def from_id(cls, sheet_id: str) -> Self:
        """Instantiate Spreadsheet with sheet ID.

        Args:
            sheet_id (str): ID of Sheet (last part of sheet url)

        Raises:
            SystemExit: Raises Exception if no spreadsheet with id could be found.

        Returns:
            Self: Returns Spreadsheet instance
        """
        sh = cls()
        try:
            sh.sheet = sh.client.open_by_key(sheet_id)
        except gspread.exceptions.SpreadsheetNotFound as snf:
            raise SystemExit(
                f"Could not find spreadsheet with name {sheet_id}. {str(snf)}"
            ) from snf

        return sh
