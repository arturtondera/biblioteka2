import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load the environment variables from .env file
path = Path(__file__).parent / ".flaskenv"
if path.exists():
    load_dotenv(dotenv_path=path)
else:
    raise IOError(".env file not found")

class Config:
    base_path = Path(__file__).parent
    db_path = base_path / "data" / "library.db"

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{str(db_path)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = json.loads(
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS").lower()
    )
    SQLALCHEMY_ECHO = json.loads(os.getenv("SQLALCHEMY_ECHO").lower())
    DEBUG = json.loads(os.getenv("DEBUG").lower())