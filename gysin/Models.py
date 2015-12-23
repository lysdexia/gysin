# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Poesy(db.Model):
    __tablename__ = "poesy"
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(128))
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, server_default=db.func.now())

class Email(db.Model):
    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(254))
