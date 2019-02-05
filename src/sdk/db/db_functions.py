from sdk.db import database
import os
import json
from sdk.db.mongo.schema import ClassInfo
from sdk.db.mongo.schema import Section
from bson.objectid import ObjectId
from utils import logger


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
        res = ClassInfo.objects.get(
            sc=sc, cn=cn, it=it, isQuarter=isQuarter, im=im)
        return res.to_json()
    except:
        return None


def get_class_section(course, year, crn, semester):
    try:
        res = Section.objects.get(
            course=course, year=year, crn=crn[0], semester=semester
        )
        return res.to_json()
    except:
        return None


def get_and_import_class_section(course, ins, crn, sec, year, date_time,
                                 currently_enrolled, maximum_enrolled, semester):
    section = get_class_section(course, year, crn, semester)

    if section is None:
        section = database.create_course_section(
                            str(course),
                            year,
                            ins,
                            int(crn[0]),
                            crn[1],
                            sec.upper(),
                            date_time,
                            maximum_enrolled,
                            currently_enrolled,
                            semester
                            )
        section.save()
        logger.info("Created new section: {} {} {}", course, crn[0], sec.upper(), semester)
        return section

    section = json.loads(section)
    _id = ObjectId(section.get('_id').get('$oid'))

    if section.get('maxEnroll') != maximum_enrolled and maximum_enrolled != 0:
        success = Section.objects.get(id=_id).update(maxEnroll=maximum_enrolled)
        if success:
            logger.success('updated: {} with {}', _id, {'maxEnrolll': maximum_enrolled})
        else:
            logger.error('failed to update: {} with {}', _id, {'maxEnroll': maximum_enrolled})

    if section.get('enrolled') != currently_enrolled:
        success = Section.objects.get(id=_id).update(enrolled=currently_enrolled)
        if success:
            logger.success('updated: {} with {}', _id, {'enrolled': currently_enrolled})
        else:
            logger.error('failed to update: {} with {}', _id, {'enrolled': currently_enrolled})

    if section.get('meeting'):
        if section.get('meeting').get('days') != date_time.get('days') and date_time.get('days') != '':
            success = Section.objects.get(id=_id).update(meeting__days=date_time.get('days'))
            if success:
                logger.success('updated: {} with {}', _id, {'meeting__days': date_time.get('days')})
            else:
                logger.error('failed to update: {} with {}', _id, {'meeting__days': date_time.get('days')})

        if section.get('meeting').get('times') != date_time.get('times') and date_time.get('times') is not None and len(date_time.get('times')) == 2:
            success = Section.objects.get(id=_id).update(meeting__times=date_time.get('times'))
            if success:
                logger.success('updated: {} with {}', _id, {'meeting__times': date_time.get('times')})
            else:
                logger.error('failed to update: {} with {}', _id, {'meeting__times': date_time.get('times')})

    return json.loads(Section.objects.get(id=_id).to_json())

def get_class_info_by_id(id):
    try:
        res = ClassInfo.objects.get(id=ObjectId(id))
        return res.to_json()
    except:
        return None


@logger.catch
def get_and_import_info(college, isQuarter, cn, sc, it, title, cr, im):
    c = get_class_info(sc, cn, it, isQuarter, im)

    if c is None:
        logger.error('{} {} {} {} {} not found', sc, cn, it, isQuarter, im)
        try:
            c = ClassInfo(college=college, isQuarter=isQuarter, cn=cn, sc=sc,
                          it=it, title=title, cr=cr, im=im).save().to_json()
            logger.success('{} {} {} {} {} created', sc, cn, it, isQuarter, im)
        except:
            logger.critical('{} {} {} {} {} failed. Perhaps the connection to the db is severed',
                            sc, cn, it, isQuarter, im)
            return ''
    c = json.loads(c)
    if c.get('cr') != cr and cr != 0:
        success = ClassInfo.objects.get(id=ObjectId(c.get('_id').get('$oid'))).update(cr=cr)
        logger.info('Success value: {}', success)
        if success:
            logger.success('updated: {} with {}', c.get('_id'), {'cr': cr})
        else:
            logger.success('failed to update: {} with {}', c.get('_id'), {'cr': cr})
    c = ObjectId(c.get('_id').get('$oid'))
    logger.info('ID: {}', c)

    return c


def import_to_db_single(college_name, _class, class_meta):
    course_id = get_and_import_info(
        college_name,
        '-Q' in class_meta,
        _class.get('CN'),
        _class.get('SC').upper(),
        _class.get('IT'),
        _class.get('CT'),
        float(_class.get('CR')) if _class.get('CR') else 0.0,
        _class.get('IM')
    )

    section = get_and_import_class_section(
        str(course_id),
        _class.get('IN'),
        _class.get('CRN'),
        _class.get('SEC').upper(),
        int(class_meta[4:].split('_')[0]),
        create_dt_obj(_class.get('DT')),
        int(_class.get('ENROLLED')) if _class.get(
            'ENROLLED') else 0,
        int(_class.get('MAX')) if _class.get('MAX') else 0,
        str(class_meta.split('-')[0]).upper(),
    )
    return section

def import_to_db_bulk(json_data, fname):
    j = json.loads(json_data)
    for college in j:
        college_name = college.get('collegeName')

        for class_category in college.get('collegeSubcategories'):
            # the "college" the class is in
            subsection_name = class_category.get('classesCategory')

            for _class in class_category.get('classes'):
                if _class.get('index') == 0:
                    continue
                
                import_to_db_single(college_name, _class, fname)

                

def import_to_db(json_data, fname):
    j = json.loads(json_data)
    for college in j:
        college_name = college.get('collegeName')

        for class_category in college.get('collegeSubcategories'):
            # the "college" the class is in
            subsection_name = class_category.get('classesCategory')

            for _class in class_category.get('classes'):
                if _class.get('index') == 0:
                    continue

                course_id = get_and_import_info(
                    college_name,
                    '-Q' in fname,
                    _class.get('CN'),
                    _class.get('SC').upper(),
                    _class.get('IT'),
                    _class.get('CT'),
                    float(_class.get('CR')) if _class.get('CR') else 0.0,
                    _class.get('IM')
                )

                course = get_and_import_class_section(
                    str(course_id),
                    _class.get('IN'),
                    _class.get('CRN'),
                    _class.get('SEC').upper(),
                    int(fname[4:].split('_')[0]),
                    create_dt_obj(_class.get('DT')),
                    int(_class.get('ENROLLED')) if _class.get(
                        'ENROLLED') else 0,
                    int(_class.get('MAX')) if _class.get('MAX') else 0,
                    str(fname.split('-')[0]).upper(),
                )


if __name__ == '__main__':
    for fname in os.listdir('./dist/.tmp'):
        with open('./dist/.tmp/' + fname) as file:
            import_to_db(file, fname)
