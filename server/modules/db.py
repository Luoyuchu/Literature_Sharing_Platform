from flask import current_app
from pymongo import MongoClient


db = None

def get_db():
    global db
    if db is None:
        client = MongoClient(current_app.config["MONGO_URI"])
        db=getattr(client, current_app.config["MONGO_DATABASE"])
    return db

