from . import mongo
import os
from dotenv import load_dotenv

try:
    load_dotenv()
except:
    pass

database = mongo.mongo_database.MongoDatabase(os.environ['MONGO_URI'])
