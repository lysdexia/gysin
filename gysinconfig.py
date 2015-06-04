import os
import cjson
_basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

CONNECT =  "mongolab connect string"
DB = "heroku_app99999999"

# some words to make a chain with
with open("words.json", "r") as f:
    WORDS = cjson.decode(f.read())

del os
