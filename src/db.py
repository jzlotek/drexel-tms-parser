from db import database
import datetime
import os
import json
from db.schema.class_section import Section
from db.schema.class_info import ClassInfo
from bson.objectid import ObjectId

# print(dir(Section))
print(database.create_course_section.__doc__)

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
        c = ClassInfo(college=college, isQuarter=isQuarter, cn=cn, sc=sc, it=it, title=title, cr=cr, im=im).save().to_json()
    
    c = ObjectId(json.loads(c).get('_id').get('$oid'))

    return c
   

# print(get_class_info("test","test","test",True))
# print(get_class_info_by_id("5c0ab91dd6a02515285f9122"))
# print(get_and_import_info("test",False,"test","test","test","test",3.0))


# exit(0)

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
                            _class.get('SC'),
                            _class.get('IT'),
                            _class.get('CT'),
                            float(_class.get('CR')) if _class.get('CR') else 0.0,
                            get_instruction_method(_class.get('IM'))
                        )
                        print(course_id)
                        course = database.create_course_section(
                            str(course_id),
                            int(fname[4:].split('_')[0]),
                            _class.get('IN'),
                            _class.get('CRN')[0],
                            _class.get('CRN')[1],
                            _class.get('SEC'),
                            create_dt_obj(_class.get('DT')),
                            int(_class.get('MAX')) if _class.get('MAX') else 0,
                            int(_class.get('ENROLLED')) if _class.get('ENROLLED') else 0
                        )
                        course.save()
                    except ValueError as e:
                        print('CR', _class.get('CR'))
                        exit(0)
