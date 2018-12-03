from db.database_interface import Database
from bson.codec_options import CodecOptions
from bson.raw_bson import RawBSONDocument
from mongoengine import connect
import pymongo.errors
from pymongo import collection
from pymongo import read_preferences
import datetime
from db.schema.class_section import Section

class MongoDatabase(Database):

    def __init__(self, db):
        super().__init__()

        try:
            self.db = connect(host=db, read_preference=read_preferences.Primary())['__socket_for_writes']
        except pymongo.errors.InvalidURI as e:
            print('{} is an invalid URI\n\n{}\n'.format(db, e))

        if not self.db.connect:
            self.logger().warning('{}'.format(str(db)))

    def create_table(self, table_name, *args, **kwargs):
        try:
            collection.Collection(self.db,
                                  table_name,
                                  create=True,
                                  codec_options=CodecOptions(document_class=RawBSONDocument))
        
            self.logger().info("Table: {} created at: {} on {}".format(table_name, datetime.datetime.now(), self.db.host))
        except AttributeError as e:
            self.logger().info("{} | Error creating {}\n{}".format(datetime.datetime.now(), table_name, e))
            print("{} | Error creating {}\n{}".format(datetime.datetime.now(), table_name, e))
            return False
        finally:
            self.logger().info("{} | Error creating {}\n".format(datetime.datetime.now(), table_name))
            print("{} | Error creating {}\n".format(datetime.datetime.now(), table_name))
            return False


        return True

    def get_table(self, table_name, *args, **kwargs):
        col = collection.Collection(self.db,
                                    table_name,
                                    codec_options=CodecOptions(document_class=RawBSONDocument))
        return col

    def find_one(self, table_name, query, *args, **kwargs):
        table = self.get_table(table_name)
        return table.find_one(query)

    def find_many(self, table_name, query, *args, **kwargs):
        table = self.get_table(table_name)
        return table.find_many(query)

    def update_data(self, table_name, data, *args, **kwargs):
        pass

    def insert(self, table_name, data, *args, **kwargs):
        table = self.get_table(table_name)

        if not table:
            return False

        if isinstance(data, list) or isinstance(data, tuple):
            table.insert_many(data)
        else:
            table.insert_one(data)

    @staticmethod
    def create_course_section(
        college: str,
        year: int,
        instructor: str,
        isQuarter: bool,
        crn: int,
        crnLink: str,
        cn: str,
        sc: str,
        it: str,
        im: int,
        sec: str,
        title: str,
        meeting: dict,
        cr: float,
        maxEnroll: int,
        enrolled: int):
        """
            college: College of the course
            year: The year it is (beginning in Septeber for the year)
            instructor: instructor
            isQuarter: if is quarter
            crn: CRN of the course
            crnLink: Link to the course page with more information
            cn: Course number
            sc: Subject Code i.e. UNIV, MATH, CS
            it: Lecture, Lab, Lab & Lecture, etc.
            im: 0 -> Face to Face, 1 -> Online, 2 -> Hybrid, 3 -> Community Based Learning
            sec: Section -> 101, 201, A, B
            title: Title
            meeting: {'days': 'MTWRF/TBD', 'times': [start, end]}
            cr: Credits
            maxEnroll: Int
            enrolled: Int    
        """
        course = Section(
            college=college,
            year=year,
            isQuarter=isQuarter,
            crn=crn,
            crnLink=crnLink,
            cn=cn,
            sc=sc,
            it=it,
            im=im,
            sec=sec,
            title=title,
            meeting=meeting,
            cr=cr,
            instructor=instructor,
            maxEnroll=maxEnroll,
            enrolled=enrolled
        )
        return course