import os
import cjson

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_DATABASE_NAME = os.environ.get("SQLALCHEMY_DATABASE_NAME")

APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")
ADMIN_SECRET_KEY = os.environ.get("ADMIN_SECRET_KEY")

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

USER_TIMEOUT = 0

# some words to make a chain with
with open("words.json", "r") as f:
    WORDS = cjson.decode(f.read())

del os
