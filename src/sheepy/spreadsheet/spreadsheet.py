"""Spreadsheet Module"""

import os
from typing import Self

import gspread
from gspread.utils import ValueInputOption, rowcol_to_a1
from requests import Response

from sheepy.util.logger import get_logger


class SheepySpreadsheet:
    """Sheepy Spreadsheet offers functionality to insert data into Google Spreadsheet"""

    HEADERS = [
        "Watched?",
        "Title",
        "Year",
        "Genre",
        "Runtime",
        "Suggested by",
        "IMDB-Score",
        "Tomatometer",
        "Director",
        "Plot",
        "Movie Poster",
    ]

    def __init__(self) -> None:
        try:
            self.client: gspread.client.Client = gspread.service_account()
        except FileNotFoundError as fnfe:
            raise SystemExit(
                f"Unable to create service account. Check credentials file. {str(fnfe)}"
            ) from fnfe
        self.spreadsheet: gspread.spreadsheet.Spreadsheet | None = None
        self.worksheet: gspread.worksheet.Worksheet | None = None
        self.spreadsheet_id: str | None = None
        self.worksheet_index: str | None = None

        self.logger = get_logger(__name__)

    @classmethod
    def from_env_file(cls) -> Self:
        """Instantiate SheepySpreadsheet from env config

        Raises:
            ValueError: Raises Exception if environment variables are not set
            SystemExit: Raises Exception if spreadsheet could not be found
            SystemExit: Raises Exception if worksheet could not be found

        Returns:
            Self: Returns new spreadsheet instance
        """
        sh = cls()
        try:
            sh.spreadsheet_id = os.environ.get("SPREADSHEET_ID")
            sh.worksheet_index = os.environ.get("WORKSHEET_INDEX")
            if sh.worksheet_index is None or sh.spreadsheet_id is None:
                sh.logger.debug(sh.spreadsheet_id)
                sh.logger.debug(sh.worksheet_index)
                raise ValueError(
                    f"One or more necessary values are None:"
                    f" {sh.spreadsheet_id=} | {sh.worksheet_index=}"
                )
            sh.spreadsheet = sh.client.open_by_key(sh.spreadsheet_id)
            sh.worksheet = sh.select_worksheet(int(sh.worksheet_index))
        except gspread.exceptions.SpreadsheetNotFound as snf:
            raise SystemExit(f"Could not find spreadsheet. {str(snf)}") from snf
        except gspread.exceptions.WorksheetNotFound as wnf:
            raise SystemExit("Can not select worksheet.") from wnf
        sh.set_instance_variables()
        sh.check_headers()
        return sh

    @classmethod
    def from_new(cls) -> Self:
        """Creates a new Spreadsheet from scratch

        Returns:
            Self: Returns new spreadsheet instance
        """
        sh = cls()
        sh.spreadsheet = sh.client.create("Sheepy_Spreadsheet")
        sh.worksheet = sh.spreadsheet.add_worksheet("Sheepy", rows=1000, cols=20)
        sh.set_instance_variables()
        sh.check_headers()
        return sh

    def set_instance_variables(self) -> None:
        """Sets variables that can not be set when instantiating

        Raises:
            ValueError: Raises Exception if there is neither spread- nor worksheet
        """
        if self.spreadsheet is None or self.worksheet is None:
            raise ValueError(
                f"One or more necessary values are None:"
                f" {self.spreadsheet=} | {self.worksheet=}"
            )
        self.spreadsheet_id = self.spreadsheet.id
        self.worksheet_index = str(self.worksheet.index)

    def setup_sheet(self) -> None:
        if self.worksheet is None:
            raise ValueError("Select a worksheet first")
        self.worksheet.update(
            range_name="A1",
            values=[list(SheepySpreadsheet.HEADERS)],
            value_input_option=ValueInputOption.user_entered,
        )

    def check_headers(self) -> None:
        if self.worksheet is None:
            raise ValueError("Select a worksheet first")
        values_list = self.worksheet.row_values(1)
        if SheepySpreadsheet.HEADERS != values_list:
            self.logger.info("Updated Headers %s", SheepySpreadsheet.HEADERS)
            self.setup_sheet()

    def transfer_ownership(self, email: str) -> None:
        """Transfer Ownership of Spreadsheet

        Args:
            email (str): Email-Address of new owner

        Raises:
            ValueError: Raises Exception if spreadsheet is not set
            ValueError: Raises Exception if email-address is not found in permissions
        """
        if self.spreadsheet is None:
            raise ValueError(
                "spreadsheet_id is None. Call set_instance_variables first"
            )
        perms: list = self.spreadsheet.list_permissions()
        perm_id = None
        for d in perms:
            if d["emailAddress"] == email:
                perm_id = d["id"]
                break
        if perm_id is None:
            raise ValueError(
                f"Could not find matching permission id for email {email=}"
            )
        resp: Response = self.spreadsheet.transfer_ownership(permission_id=perm_id)
        if resp.status_code == 200:
            self.logger.info(
                "Ownership transfer initiated."
                + "Accept in Google Spreadsheet Web Interface"
            )

    def share_spreadsheet(self, email: str, account_type: str, role: str) -> None:
        """Shares Spreadsheet with another account.

        Args:
            email (str): E-Mail of receiver-account
            account_type (str): account type of receiver account
            role (str): Role to be given to new account

        Raises:
            ValueError: raises when spreadsheet is None
        """
        if not self.spreadsheet:
            raise ValueError(
                "Can not select worksheet because there is no spreadsheet selected"
            )
        self.spreadsheet.share(email_address=email, perm_type=account_type, role=role)

    def select_worksheet(self, index: int) -> gspread.worksheet.Worksheet:
        """Selects worksheet to append values to.

        Args:
            index (int | None, optional): Index of worksheet. Defaults to None.

        Raises:
            ValueError: _description_
            ValueError: _description_
            SystemExit: _description_
            ValueError: _description_

        Returns:
            gspread.worksheet.Worksheet: Instance of Worksheet
        """
        self.logger.debug(index)
        if not self.spreadsheet:
            raise ValueError(
                "Can not select worksheet because there is no spreadsheet selected"
            )
        worksheet: gspread.worksheet.Worksheet | None = None
        try:
            worksheet = self.spreadsheet.get_worksheet(index)
        except gspread.exceptions.WorksheetNotFound as wnf:
            raise SystemExit(
                f"Can not select worksheet with index {index}. {str(wnf)}"
            ) from wnf
        finally:
            if worksheet is None:
                raise ValueError("Could not find any worksheets with given arguments")
        return worksheet

    def find_free_row(self) -> int:
        """Finds first row not populated with data

        Raises:
            ValueError: Raises Error if worksheet is not set

        Returns:
            int: Returns number of first free row
        """
        if not self.worksheet:
            raise ValueError("Select a worksheet first")
        row_list: list = list(filter(None, self.worksheet.col_values(2)))
        self.logger.info("First free row: %s", len(row_list) + 1)
        return len(row_list) + 1

    def add_movie_to_sheet(self, movie_dict: dict[str, str]) -> None:
        """Adds movie to spreadsheet

        Args:
            movie_dict (dict): Dictionary with movie data
        """
        if self.worksheet is None:
            raise ValueError("Select a worksheet first")
        insert_row: int = self.find_free_row()
        a1_notation: str = rowcol_to_a1(insert_row, 1)
        values: list = [list(movie_dict.values())]
        self.logger.info("A1-Notation %s", a1_notation)
        self.logger.info("%s", values)
        self.worksheet.update(
            range_name=a1_notation,
            values=values,
            value_input_option=ValueInputOption.user_entered,
        )