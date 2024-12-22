
from dotenv import load_dotenv
from os import getenv


load_dotenv()


GOOGLE_SPREADSHEET_ID = getenv('GOOGLE_SPREADSHEET_ID')
GOOGLE_SPREADSHEET_WORKSHEET_TITLE = getenv('GOOGLE_SPREADSHEET_WORKSHEET_TITLE')
SYNC_COLUMNS = getenv('SYNC_COLUMNS')
DATABASE_URL = getenv('DATABASE_URL')

ID = getenv('ID')
USERNAME = getenv('SLACK_USERNAME')
FULLNAME = getenv('FULLNAME')
PHONE = getenv('PHONE')
SUB_TYPE = getenv('SUB_TYPE')
SUB_STATUS = getenv('SUB_STATUS')
