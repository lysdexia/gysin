import datetime, uuid, random
from flask import Flask, render_template, request, url_for, g
from flask_bootstrap import Bootstrap
from flask.ext import restful
from gysin.markov import Markov

class ApeyEye(restful.Resource):

    def get(self):
        markov = Markov(app.config["WORDS"])
        return markov.chain()

app = Flask(__name__)
app.config.from_object("gysinconfig")

api = restful.Api(app)
api.add_resource(ApeyEye, "/api/chain")

@app.route("/")
def index():
    return render_template("index.html");
