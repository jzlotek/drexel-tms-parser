from db import database
import datetime
import os
import json
from db.schema.class_section import Section
from db.schema.class_info import ClassInfo
from bson.objectid import ObjectId
from utils import logger

logger.info(database.create_course_section.__doc__)


def get_instruction_method(im):
    if im == "Face to Face":
        return 0
    elif im == "Online":
        return 1
    elif im == "Hybrid":
        return 2
    else:
        return 3


def create_dt_obj(dt):
    try:
        return dict(
            days=dt.get('days'),
            times=dt.get('times')
        )
    except:
        return dict(days=dt.get('days'))


def get_class_info(sc, cn, it, isQuarter, im):
    try:
        res = ClassInfo.objects.get(sc=sc, cn=cn, it=it, isQuarter=isQuarter, im=im)
        return res.to_json()
    except:
        return None


def get_class_info_by_id(id):
    try:
        res = ClassInfo.objects.get(id=ObjectId(id))
        return res.to_json()
    except:
        return None


def get_and_import_info(college, isQuarter, cn, sc, it, title, cr, im):
    c = get_class_info(sc, cn, it, isQuarter, im)

    if c is None:
        logger.error('{} {} {} {} {} not found', sc, cn, it, isQuarter, im)
        c = ClassInfo(college=college, isQuarter=isQuarter, cn=cn, sc=sc,
                      it=it, title=title, cr=cr, im=im).save().to_json()
        logger.success('{} {} {} {} {} created', sc, cn, it, isQuarter, im)

    c = ObjectId(json.loads(c).get('_id').get('$oid'))
    logger.info('ID: {}', c)

    return c


for fname in os.listdir('./dist/.tmp'):
    with open('./dist/.tmp/' + fname) as file:
        j = json.load(file)
        for college in j:
            college_name = college.get('collegeName')

            for class_category in college.get('collegeSubcategories'):
                subsection_name = class_category.get('classesCategory')

                for _class in class_category.get('classes'):
                    if _class.get('index') == 0:
                        continue
                    try:
                        course_id = get_and_import_info(
                            college_name,
                            '-Q' in fname,
                            _class.get('CN'),
                            _class.get('SC').upper(),
                            _class.get('IT'),
                            _class.get('CT'),
                            float(_class.get('CR')) if _class.get('CR') else 0.0,
                            get_instruction_method(_class.get('IM'))
                        )

                        course = database.create_course_section(
                            str(course_id),
                            int(fname[4:].split('_')[0]),
                            _class.get('IN'),
                            _class.get('CRN')[0],
                            _class.get('CRN')[1],
                            _class.get('SEC').upper(),
                            create_dt_obj(_class.get('DT')),
                            int(_class.get('MAX')) if _class.get('MAX') else 0,
                            int(_class.get('ENROLLED')) if _class.get('ENROLLED') else 0,
                            str(fname.split('-')[0]).upper()
                        )
                        course.save()
                    except ValueError as e:
                        logger.error('CR: {}', _class.get('CR'))
                        exit(0)
