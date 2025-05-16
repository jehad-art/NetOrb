from pymongo import MongoClient
from settings import settings

client = MongoClient(settings.mongodb_uri)
db = client[settings.db_name]
devices_collection = db["devices"]