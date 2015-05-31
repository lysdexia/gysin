import os
import cjson
_basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

CONNECT = "mongodb://heroku_app37330063:5p1eoin7g4uvikko4anao29qn2@ds041432.mongolab.com:41432/heroku_app37330063"
DB = "heroku_app37330063"

# some words to make a chain with
with open("words.json", "r") as f:
    WORDS = cjson.decode(f.read())

del os
