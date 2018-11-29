import db.mongo_database as mongo_database
import db.database_interface as database_interface
import db.schema as schema

database = mongo_database.MongoDatabase('mongodb://')
