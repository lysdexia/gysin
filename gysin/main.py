import datetime, uuid, random
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, g
from flask.ext import restful
from gysin.markov import Markov

class Store(restful.Resource):
    def __init__(self):
        client = MongoClient("mongodb://heroku_app37330063:5p1eoin7g4uvikko4anao29qn2@ds041432.mongolab.com:41432/heroku_app37330063")
        self.db = client["heroku_app37330063"]

    def get(self):
        entries = self.db["entries"]
        return entries.find_one()

    def post(self):
        """
        Save a bit of posey to the database
        """
        if not request.get_json():
            abort(400);

        obj = cjson.decode(request.get_json())
        obj["datetime"] = datetime.datetime.now().isoformat()

        entries = self.db["entries"]
        post_id = entries.insert_one(obj).inserted_id
        return post_id, 201

class Chain(restful.Resource):
    def get(self):
        markov = Markov(app.config["WORDS"])
        return markov.chain()

app = Flask(__name__)
app.config.from_object("gysinconfig")

api = restful.Api(app)
api.add_resource(Chain, "/api/chain")
api.add_resource(Store, "/api/store")


@app.route("/")
def index():
    return render_template("index.html");

@app.route("/editor")
def editor():
    return render_template("editor.html");
