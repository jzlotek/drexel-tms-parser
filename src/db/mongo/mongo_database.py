from db.database_interface import Database
from mongoengine import connect
import pymongo.errors
from pymongo import read_preferences
from db.mongo.schema import Section
from db.mongo.schema import ClassInfo
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
        query = {'year': int(year)}
        self.query.update(query)

    def section(self, section):
        self.query.update({'sec': section})

    def crn(self, crn):
        self.query.update({'crn': int(crn)})

    def meeting(self, meeting, type_):
        if type_ == 'days':
            accepted = 'MTWRF'
            if meeting.upper() == "TBD":
                query = {'meeting': {'days': meeting}}
                self.query.update(query)
                return
            for index, letter in enumerate(meeting):
                if letter not in accepted:
                    meeting.splice(index, 1)

            query = {'meeting': {'days': meeting}}
            self.query.update(query)

    def instructor(self, instructor):
        self.query.update({'instructor': instructor})

    def college(self, college):
        self.query.update({'college': college})

    def course_number(self, cn):
        self.query.update({'cn': cn})

    def subject_code(self, sc):
        query = {'sc': sc}
        self.query.update(query)

    def instruction_type(self, it):
        self.query.update({'it': it})

    def instruction_method(self, im):
        self.query.update({'im': int(im)})

    def credits(self, cr):
        self.query.update({'cr': float(cr)})

    def before(self, time):
        self.query.update({'before': time})

    def after(self, time):
        self.query.update({'after': time})

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
            'instructor',
            'year',
            'sec',
            'crn',
            'before',
            'after'
        ]
        meeting_dict = dict()
        meeting_fields = [
            'meeting'
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
                return []

            return section

        for key, value in self.query.items():
            logger.debug('key: {}, value: {}', key, value)
            if key in info_fields:
                info_dict.update({key: value})
            elif key in section_fields:
                section_dict.update({key: value})
            elif key in meeting_fields:
                meeting_dict.update({key: value})
            else:
                logger.error('Unknown key/value pair: ', key, value)
        meeting_dict = meeting_dict.get('meeting')
        
        if not section_dict.get('year'):
            # fall back to current year
            import datetime
            now = datetime.datetime.now()
            year = now.year % 2000
            if now.month < 9:
                year -= 1
            section_dict.update({'year': year})
        
        if len(info_dict.items()) != 0:
            course_info_list = json.loads(
                ClassInfo.objects(__raw__=info_dict).to_json()
            )
            logger.debug('course_info_list: {}', course_info_list)
            course_id_list = [
                c.get('_id').get('$oid') for c in course_info_list
            ]

            if meeting_dict and meeting_dict.get('days') is not None and len(meeting_dict.get('days')) > 0:
                course_sections = json.loads(
                    Section.objects(
                        meeting__days=meeting_dict.get('days'),
                        course__in=course_id_list,
                        __raw__=section_dict
                    ).to_json()
                )
            else:
                course_sections = json.loads(
                    Section.objects(
                        course__in=course_id_list,
                        __raw__=section_dict
                    ).to_json()
                )

            for section in course_sections:
                course_info = list(
                    filter(
                        lambda ci: ci.get('_id').get(
                            '$oid') == section.get('course'),
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

    def get_query(self):
        return self.query
    
    def get_list(self, l, query=None):
        # subject-codes
        # course-number
        # colleges
        # years
        if l == "subject-codes":
            codes = sorted(list(set([c.sc for c in ClassInfo.objects()])))
            logger.info(codes)
            return codes
        elif l == "course-number":
            self.subject_code(query.get('sc'))
            self.year(query.get('year') if query.get('year') else 18)
            classes = self.execute()
            return sorted(list(set([c.get('course').get('cn') for c in classes])))
        elif l == "years":
            return sorted(list(set([c.year for c in Section.objects()])))
        return []

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
            enrolled: int,
            semester: str):
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
            enrolled=enrolled,
            semester=semester
        )
        return course
