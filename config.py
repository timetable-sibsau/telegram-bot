import os
from dotenv import load_dotenv

# loading .env file content as a system environment variable
load_dotenv()

# getting values from environment variable
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
SUPPORT = os.getenv('SUPPORT_USERNAME')
BOT_VERSION = os.getenv('BOT_VERSION')
DB_FILE = os.getenv('DB_FILE_PATH')
GROUPS_FILE = os.getenv('GROUPS_FILE_PATH')
PATH_TO_TT_FILES = os.getenv('TIMETABLE_FILES_PATH')
DOMAIN = os.getenv('DOMAIN_ADDRESS')
HEADERS = os.getenv('USER_AGENT_HEADERS')

print(f'{TOKEN}\n{ADMIN_ID}\n{SUPPORT}\n{BOT_VERSION}\n{DB_FILE}\n{GROUPS_FILE}\n{PATH_TO_TT_FILES}\n{DOMAIN}'
      f'\n{HEADERS}')
