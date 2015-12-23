# -*- coding: utf-8 -*-
from flask import Flask
from flaskext.markdown import Markdown
from gysin.Models import db
from gysin.Roles import auth_roles
from gysin.Routes import routes
from gysin.Poesy import api
from gysin.MarkovChainGenerator import Markov

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config["APP_SECRET_KEY"]

# add markdown filter
Markdown(app)

# initialize db on app
db.init_app(app)

# add authentication roles 
auth = auth_roles(app)

# routes require database
routes(app, db)

# markov chain generator
markov = Markov(app.config["WORDS"])

# api requires db and markov chain generator
api(app, db, markov)
