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
import copy
from utils import logger

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
            logger.error('{} is an invalid URI\n\n{}\n'.format(db, e))

        if not self.db.connect:
            logger.warning('{}'.format(str(db)))
        else:
            logger.success('{}'.format(str(self.db)))


    def year(self, year):
        query = {'year': year}
        logger.debug(query)
        self.query.update(query)
    
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
                logger.error(error)
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
            course_info_list = json.loads(ClassInfo.objects(__raw__=info_dict).to_json())
            course_id_list = [
                c.get('_id').get('$oid') for c in course_info_list
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
                        lambda ci: ci.get('_id').get('$oid') == section.get('course'),
                        course_info_list
                    )
                )
                if len(course_info) == 1:
                    tmp_course = copy.deepcopy(course_info[0])
                    if tmp_course.get('_id'):
                        del tmp_course['_id']

                    section.update({'course': tmp_course})
                
                if section.get('_id'):
                    del section['_id']

            
            return course_sections

        


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