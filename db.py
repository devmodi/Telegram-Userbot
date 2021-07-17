import pymongo
from pymongo import MongoClient
from config import CONNECTION_STRING

client = MongoClient(CONNECTION_STRING)
db = client.telegramDatabase
collection = db.telegramCollection


def save_posts_in_db(posts):
    collection.insert_many(posts)


def get_users_from_db():
    usernames = []
    for post in collection.find():
        usernames.append(post['username'])
    return usernames
