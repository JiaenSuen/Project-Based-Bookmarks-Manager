import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent.parent

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INSTANCE_PATH = basedir / 'instance'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{Config.INSTANCE_PATH / 'bookmarks-dev.db'}"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{Config.INSTANCE_PATH / 'bookmarks.db'}"
    

