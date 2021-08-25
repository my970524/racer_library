import os

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = 'affsfsfsdf'

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/racer_library"

SQLALCHEMY_TRACK_MODIFICATIONS = False