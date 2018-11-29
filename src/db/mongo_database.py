from db.database_interface import Database
from mongoengine import connect
import pymongo.errors


class MongoDatabase(Database):

    def __init__(self, db):
        super().__init__()

        try:
            self.db = connect(host=db)
        except pymongo.errors.InvalidURI as e:
            print('{} is an invalid URI\n\n{}\n'.format(db, e))

        if not self.db.connect:
            self.logger().warning('{}'.format(str(db)))

    def create_table(self, table_name, *args, **kwargs):
        pass

    def get_table(self, table_name, *args, **kwargs):
        pass

    def update_data(self, table_name, data, *args, **kwargs):
        pass
