
import gspread
from gspread.utils import ValueInputOption


class GoogleSpreadsheet:
    def __init__(self, spreadsheet_id: str, worksheet_title: str):
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_title = worksheet_title
        gc = gspread.service_account(filename='creds.json')
        self.spreadsheet = gc.open_by_key(key=self.spreadsheet_id)
        self.sheet = self.spreadsheet.worksheet(title=self.worksheet_title)

    def get_all(self, start_row: int = 0) -> list:
        values = self.sheet.get_all_values()
        if len(values) < start_row:
            return []
        for row in values[start_row:]:
            if row and row[0].isdigit():
                row[0] = int(row[0])
        return values[start_row:]

    def append_row(self, values: list) -> None:
        self.sheet.append_row(
            values=values,
            value_input_option=ValueInputOption.user_entered,
        )

    def update_row_by_index(self, index: int, values: list) -> None:
        self.sheet.update(
            values=[values],
            range_name=f'A{index}:{chr(64+len(values))}{index}',
            value_input_option=ValueInputOption.user_entered,
        )