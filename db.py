import pymongo
from pymongo import MongoClient
from config import CONNECTION_STRING

client = MongoClient(CONNECTION_STRING)
db = client.telegramDatabase
collection = db.telegramCollection


def save_db(post):
    collection.insert_one(post)

def get_db():
    usernames = []
    for post in collection.find():
        usernames.append(post['username'])
    return usernames
