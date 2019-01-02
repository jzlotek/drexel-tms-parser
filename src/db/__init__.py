from . import mongo
import os
from dotenv import load_dotenv
from pathlib import Path
from utils import logger

try:
    dotenv_path = Path('../..') / '.env'
    load_dotenv(dotenv_path=dotenv_path)
except:
    logger.error(".env not found in root directory")

MONGO_URI = os.environ.get('MONGO_URI') if os.environ.get('MONGO_URI') else ''

if MONGO_URI == '':
    logger.critical('Environment variable MONGO_URI was not found')

database = mongo.mongo_database.MongoDatabase(MONGO_URI)
