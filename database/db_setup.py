import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

import sqlalchemy  # type: ignore
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy_utils import database_exists, create_database  # type: ignore

from urllib.parse import quote_plus

port = os.environ.get("DB_PORT")
password = os.environ.get("DB_PWD")
encoded_password = quote_plus(str(password))
db_to_connect = os.environ.get("DB_NAME")

engine = create_engine(
    f"postgresql://postgres:{encoded_password}@localhost:5432/{db_to_connect}",
    echo=False,
)

if not database_exists(engine.url):
    create_database(engine.url)

if database_exists(engine.url):
    print(f"{db_to_connect} database connected successfully")
else:
    print(f"could not connect to {db_to_connect} database")
