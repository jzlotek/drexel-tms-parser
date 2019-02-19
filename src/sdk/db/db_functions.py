from sdk.db import database
import os
import json
from sdk.db.mongo.schema import ClassInfo
from sdk.db.mongo.schema import Section
from bson.objectid import ObjectId
from utils import logger


def get_class_info(sc, cn, it, im):
    try:
        res = ClassInfo.objects.get(
            sc=sc, cn=cn, it=it, im=im)
        return res.to_json()
    except:
        return None


def get_class_section(course, year, crn, semester, isQuarter):
    try:
        res = Section.objects.get(
            course=course, year=year, crn=crn[0], semester=semester, isQuarter=isQuarter
        )
        return res.to_json()
    except:
        return None


def get_and_import_class_section(course, ins, crn, sec, year, date_time,
                                 currently_enrolled, maximum_enrolled, semester, isQuarter):
    section = get_class_section(course, year, crn, semester, isQuarter)

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
                            semester,
                            isQuarter
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
        if section.get('meeting').get('TBD') and date_time.get('TBD'):
            success = Section.objects.get(id=_id).update(meeting=date_time)
            if success:
                logger.success('updated: {} with {}', _id, {'meeting': date_time})
            else:
                logger.error('failed to update: {} with {}', _id, {'meeting': date_time})
        elif not section.get('meeting').get('TBD') and date_time.get('TBD'):
            # check differences
            tmp_meeting = {}
            changes = False
            for key, value in date_time.items():
                if (not section.get('meeting').get(key) and value.get('start') > 0 and value.get('end') > 0) or\
                    (section.get('meeting').get(key) != value and value.get('start') > 0 and value.get('end') > 0):
                    tmp_meeting.update({key, value})
                    changes = True
                else:
                    tmp_meeting.update({key, section.get('meeting').get(key)})
            
            if changes:
                success = Section.objects.get(id=_id).update(meeting=tmp_meeting)
                if success:
                    logger.success('updated: {} with {}', _id, {'meeting': date_time})
                else:
                    logger.error('failed to update: {} with {}', _id, {'meeting': date_time})

    return json.loads(Section.objects.get(id=_id).to_json())

def get_class_info_by_id(id):
    try:
        res = ClassInfo.objects.get(id=ObjectId(id))
        return res.to_json()
    except:
        return None


@logger.catch
def get_and_import_info(college, cn, sc, it, title, cr, im):
    c = get_class_info(sc, cn, it, im)

    if c is None:
        logger.error('{} {} {} {} not found', sc, cn, it, im)
        try:
            c = ClassInfo(college=college, cn=cn, sc=sc,
                          it=it, title=title, cr=cr, im=im).save().to_json()
            logger.success('{} {} {} {} created', sc, cn, it, im)
        except:
            logger.critical('{} {} {} {} failed. Perhaps the connection to the db is severed',
                            sc, cn, it, im)
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
        _class.get('cn'),
        _class.get('sc').upper(),
        _class.get('it'),
        _class.get('title'),
        float(_class.get('cr')) if _class.get('cr') else 0.0,
        _class.get('im')
    )

    section = get_and_import_class_section(
        str(course_id),
        _class.get('ins'),
        _class.get('crn'),
        _class.get('sec').upper(),
        int(class_meta[4:].split('_')[0]),
        _class.get('meeting'),
        int(_class.get('enrolled')) if _class.get(
            'enrolled') else 0,
        int(_class.get('maxEnroll')) if _class.get('maxEnroll') else 0,
        str(class_meta.split('-')[0]).upper(),
        '-Q' in class_meta
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
                _class.get('cn'),
                _class.get('sc').upper(),
                _class.get('it'),
                _class.get('title'),
                float(_class.get('cr')) if _class.get('cr') else 0.0,
                _class.get('im')
            )

            section = get_and_import_class_section(
                str(course_id),
                _class.get('ins'),
                _class.get('crn'),
                _class.get('sec').upper(),
                int(fname[4:].split('_')[0]),
                _class.get('meeting'),
                int(_class.get('enrolled')) if _class.get(
                    'enrolled') else 0,
                int(_class.get('maxEnroll')) if _class.get('maxEnroll') else 0,
                str(fname.split('-')[0]).upper(),
                '-Q' in fname
            )


if __name__ == '__main__':
    for fname in os.listdir('./dist/.tmp'):
        with open('./dist/.tmp/' + fname) as file:
            import_to_db(file, fname)
