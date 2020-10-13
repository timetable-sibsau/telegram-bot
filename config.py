import os
import json
from environs import Env

# loading .env file content as a system environment variable
env = Env()
env.read_env()

# getting values from environment variable
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = env.list('ADMIN_ID')
SUPPORT = os.getenv('SUPPORT_USERNAME')
BOT_VERSION = os.getenv('BOT_VERSION')
DB_FILE = os.getenv('DB_FILE_PATH')
GROUPS_FILE = os.getenv('GROUPS_FILE_PATH')
PATH_TO_TT_FILES = os.getenv('TIMETABLE_FILES_PATH')
DOMAIN = os.getenv('DOMAIN_ADDRESS')
HEADERS = json.loads(os.getenv('USER_AGENT_HEADERS'))
FILE_LOGGING_MODE = env.bool('FILE_LOGGING_MODE')
