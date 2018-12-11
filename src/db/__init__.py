import db.mongo_database as mongo_database
import db.database_interface as database_interface
import db.schema as schema
import os
from dotenv import load_dotenv
from pathlib import Path

try:
    load_dotenv()
except:
    pass

database = mongo_database.MongoDatabase(os.environ['MONGO_URI'])
