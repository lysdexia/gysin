# -*- coding: utf-8 -*-
import datetime, uuid, random
from flask import g
from flask.ext import restful

def api(app, db, markov):

    api = restful.Api(app)
    class Chain(restful.Resource):
        """
        Handle markov chains.
        """
        def get(self):
            """
            generate a new random chain
            returns list of gibberish
            TODO global object since this is read-only?
            """
            return markov.chain()

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

    api.add_resource(Chain, "/api/chain")
    api.add_resource(View, "/api/view/<poesy_id>")
