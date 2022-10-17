
from config import settings
from pymongo import MongoClient


client = MongoClient(settings.mongo_url)
db = client.recipes

