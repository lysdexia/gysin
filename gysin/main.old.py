# -*- coding: utf-8 -*-
import datetime, uuid, random
import cjson
from pymongo import MongoClient
from bson import json_util, ObjectId
from flask import Flask, render_template, request, url_for, g
from flask.ext import restful
from gysin.markov import Markov

class View(restful.Resource):
    """
    View stored o-pus-seas
    """
    def __init__(self):
        self.client = MongoClient(app.config["MONGOLAB_URI"])
        self.db = self.client[app.config["MONGOLAB_DB"]]

    def get(self, poesy_id):
        """
        accepts poesy_id, vis:
        //foo.tld/api/view/556a563d122704575e4d15c7
        returns error and 400 if bad
        returns json object and 200 if ok
        """
        entries = self.db["entries"]
        try:
            obj = entries.find_one({"_id": ObjectId(poesy_id)})
        except Exception as e:
            self.client.close()
            return "Invalid id: %s"%str(e), 400
        try:
            poesy = json_util.dumps(obj)
        except Exception as e:
            self.client.close()
            return "Bad data: %s"%str(e), 400

        self.client.close()
        return poesy, 200

class Store(restful.Resource):
    """
    Store text to db
    """
    def __init__(self):
        self.client = MongoClient(app.config["CONNECT"])
        self.db = self.client[app.config["DB"]]

    def post(self, poesy_id=None):
        """
        post a bit of poesy to the database
        return error, 400 if fail
        return post_id, 201 if ok
        """
        if not request.get_json():
            self.client.close()
            return "cannot extract json from whatever you sent", 400

        obj = request.get_json()
        obj["datetime"] = datetime.datetime.now().isoformat()

        entries = self.db["entries"]
        post_id = entries.insert_one(obj).inserted_id
        self.client.close()
        return str(post_id), 201

class Chain(restful.Resource):
    """
    Handle markov chains.
    """
    def get(self):
        """
        generate a new random chain
        returns list of gibberish
        """
        markov = Markov(app.config["WORDS"])
        return markov.chain()

app = Flask(__name__)

app.config.from_object("config")

api = restful.Api(app)
api.add_resource(Chain, "/api/chain")
api.add_resource(Store, "/api/store")
api.add_resource(View, "/api/view/<poesy_id>")

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/editor")
def editor():
    return render_template("editor.html");

@app.route("/poesy/<poesy_id>")
def poesy(poesy_id): 
    client = MongoClient(app.config["CONNECT"])
    db = client[app.config["DB"]]
    entries = db["entries"]
    try:
        obj = entries.find_one({"_id": ObjectId(poesy_id)})
    except Exception as e:
        client.close()
        return render_template("error.html")
    poesy = {
            "title": obj["title"],
            "author": obj["author"],
            "datetime": obj["datetime"],
            "poesy": "<br>".join(obj["poesy"].split("\n")),
            }
    client.close()
    return render_template("poesy.html", poesy=poesy)
