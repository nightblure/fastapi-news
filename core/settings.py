import os
from pathlib import Path
from dotenv import load_dotenv
from starlette.templating import Jinja2Templates

DEBUG = False

ROOT_DIR = Path(__file__).resolve().parent.parent
dotenv_path = ROOT_DIR / '.env'

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise Exception('.env-файл со значениями переменных окружения не найден!')

BASE_URL = 'http://127.0.0.1:8000'

FROM_DOCKER_IMAGE = os.environ.get('FROM_DOCKER_IMAGE')

REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_HOST = 'localhost'

DB_HOST = os.environ.get('DB_HOST')

if FROM_DOCKER_IMAGE:
    REDIS_HOST = os.environ.get('REDIS_DOCKER_IMAGE_HOST')
    DB_HOST = os.environ.get('DB_DOCKER_IMAGE_HOST')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}' # psycopg2

if DEBUG:
    print(f'DATABASE_URL: {DATABASE_URL}')


templates = Jinja2Templates(directory='templates')