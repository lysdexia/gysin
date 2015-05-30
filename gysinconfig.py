import os
import cjson
_basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

# some words to make a chain with
with open("words.json", "r") as f:
    WORDS = cjson.decode(f.read())

del os
