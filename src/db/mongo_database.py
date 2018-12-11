from db.database_interface import Database
from bson.codec_options import CodecOptions
from bson.raw_bson import RawBSONDocument
from mongoengine import connect
import pymongo.errors
from pymongo import collection
from pymongo import read_preferences
import datetime
from db.schema.class_section import Section
from db.schema.class_info import ClassInfo
from bson import ObjectId
import json
import mongoengine.errors

class MongoDatabase(Database):

    def __init__(self, db):
        super().__init__()
        self.query = dict()

        try:
            self.db = connect(
                host=db,
                read_preference=read_preferences.Primary()
            )['__socket_for_writes']

        except pymongo.errors.InvalidURI as e:
            print('{} is an invalid URI\n\n{}\n'.format(db, e))

        if not self.db.connect:
            self.logger().warning('{}'.format(str(db)))


    def year(self, year):
        self.query.update({'year': year})
    
    def section(self, section):
        self.query.update({'sec': section})
    
    def crn(self, crn):
        self.query.update({'crn': crn})
    
    def meeting(self, meeting):
        self.query.update({'meeting': meeting})

    def instructor(self, instructor):
        self.query.update({'instructor': instructor})
    
    def college(self, college):
        self.query.update({'college': college})
    
    def course_number(self, cn):
        self.query.update({'cn': cn})

    def subject_code(self, sc):
        self.query.update({'sc': sc})
    
    def instruction_type(self, it):
        self.query.update({'it': it})

    def instruction_method(self, im):
        self.query.update({'im': im})
    
    def credits(self, cr):
        self.query.update({'cr': cr})

    def execute(self):
        info_dict = dict()
        info_fields = [
            'cr',
            'college',
            'it',
            'im',
            'sc',
            'cn'
        ]
        section_dict = dict()
        section_fields = [
            'meeting',
            'instructor',
            'year',
            'sec',
            'crn'
        ]

        # handle CRN only lookup
        if self.query.get('crn') is not None:
            try:
                section = json.loads(
                    Section.objects.get(crn=self.query.get('crn')).to_json()
                )
                course_id = section.get('course')

                course = ClassInfo.objects.get(
                    id=ObjectId(course_id)
                ).to_json()

                section.update({'course': course})
            except mongoengine.errors.DoesNotExist as error:
                self.logger().error(error)
                return None

            return section

        for key, value in self.query.items():
            if key in info_fields:
                info_dict.update({key: value})
            elif key in section_fields:
                section_dict.update({key: value})
            else:
                print('Unknown key/value pair: ', key, value)
        
        if len(info_dict.items()) != 0:
            course_info_list = ClassInfo.objects(__raw__=info_dict)
            course_id_list = [
                json.loads(c).get('_id').get('$oid') for c in course_info_list
            ]

            course_sections = json.loads(
                Section.objects(
                    course__in=course_id_list,
                    __raw__=section_dict
                ).to_json()
            )

            for section in course_sections:
                course_info = list(
                    filter(
                        lambda ci: json.loads(ci).get('_id').get('$oid') == section.get('course'),
                        course_info_list
                    )
                )
                if len(course_info) == 1:
                    section.update({'course': course_info})

        


        self.query = dict()

    def get_query(self):
        return self.query

    @staticmethod
    def create_course_section(
        course: str,
        year: int,
        instructor: str,
        crn: int,
        crnLink: str,
        sec: str,
        meeting: dict,
        maxEnroll: int,
        enrolled: int):
        """
            course: ObjectId of the course
            year: The year it is (beginning in Septeber for the year)
            instructor: instructor
            crn: CRN of the course
            crnLink: Link to the course page with more information
            sec: Section -> 101, 201, A, B
            meeting: {'days': 'MTWRF/TBD', 'times': [start, end]}
            maxEnroll: Int
            enrolled: Int    
        """
        course = Section(
            course=course,
            year=year,
            crn=crn,
            crnLink=crnLink,
            sec=sec,
            meeting=meeting,
            instructor=instructor,
            maxEnroll=maxEnroll,
            enrolled=enrolled
        )
        return course