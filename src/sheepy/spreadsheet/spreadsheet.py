"""Spreadsheet Module"""

import os
from typing import Any, Self

import gspread
from gspread.utils import ValueInputOption, rowcol_to_a1
from requests import Response

from sheepy.util.logger import get_logger

from .formatting import (
    check_headers,
    set_insert_row_height,
    setup_checkboxes,
    setup_sheet_formatting,
)


class SheepySpreadsheet:
    """Sheepy Spreadsheet offers functionality to insert data into Google Spreadsheet"""

    def __init__(
        self, spreadsheet_id: str | None = None, worksheet_index: str | None = None
    ) -> None:
        """Constructor of Spreadsheet

        Args:
            spreadsheet_id (str | None, optional): ID of Spreadsheet. Defaults to None.
            worksheet_index (str | None, optional): Worksheet Index. Defaults to None.

        Raises:
            ValueError: _description_
            SystemExit: _description_
            SystemExit: _description_
            SystemExit: _description_
        """
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

        if (spreadsheet_id is None) != (worksheet_index is None):
            raise ValueError("Please provide spreadsheet ID and worksheet index")
        elif spreadsheet_id is not None and worksheet_index is not None:
            try:
                self.spreadsheet_id = spreadsheet_id
                self.worksheet_index = worksheet_index
                self.spreadsheet = self.client.open_by_key(spreadsheet_id)
                self.worksheet = self.select_worksheet(int(worksheet_index))
                check_headers(self)
            except gspread.exceptions.SpreadsheetNotFound as snf:
                raise SystemExit(f"Could not find spreadsheet. {str(snf)}") from snf
            except gspread.exceptions.WorksheetNotFound as wnf:
                raise SystemExit("Can not select worksheet.") from wnf

    def __repr__(self):
        return (
            f"Spreadsheet ID: {self.spreadsheet_id}\n"
            f"Worksheet index: {self.worksheet_index}"
        )

    @classmethod
    def from_env_file(cls) -> Self:
        """Instantiate SheepySpreadsheet from environment variable config

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
        check_headers(sh)
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
        setup_sheet_formatting(sh)
        check_headers(sh)
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
        perm_id: Any = None
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

    def read_row(self, row_number: int) -> list[Any]:
        """Reads Value of a row

        Args:
            row_number (int): Row Number

        Returns:
            list[Any]: Returns list of values present in row
        """
        if self.worksheet is None:
            raise ValueError("Worksheet of SheepySpreadsheet object is not set.")
        return self.worksheet.row_values(row_number)

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

    def add_values_to_sheet(self, movie_dict: dict) -> None:
        """_summary_

        Args:
            movie_dict (dict): _description_

        Raises:
            ValueError: _description_
        """
        if self.worksheet is None:
            raise ValueError("Select a worksheet first")
        insert_row: int = self.find_free_row()
        a1_notation: str = rowcol_to_a1(insert_row, 1)
        values: list[list[str]] = [list(movie_dict.values())]
        self.logger.debug("A1-Notation %s", a1_notation)
        self.logger.debug("%s", values)
        setup_checkboxes(ss=self, cell=f"A{insert_row}")
        set_insert_row_height(ss=self, row=insert_row)
        self.worksheet.update(
            range_name=a1_notation,
            values=values,
            value_input_option=ValueInputOption.user_entered,
        )
        self.logger.info(
            f"\n{'#' * 60}\n"
            f"Added Movie Info: {movie_dict}\n"
            f"to Spreadsheet:\n{self}\n"
            f"{'#' * 60}\n"
        )
