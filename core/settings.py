import os
from pathlib import Path
from dotenv import load_dotenv

DEBUG = True

ROOT_DIR = Path(__file__).resolve().parent.parent
dotenv_path = ROOT_DIR / '.env'

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise Exception('.env-файл со значениями переменных окружения не найден!')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

if DEBUG:
    print(f'DATABASE_URL: {DATABASE_URL}')
