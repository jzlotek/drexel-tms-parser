from db import database
import datetime
import os
import json
from db.schema.class_section import Section

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


for fname in os.listdir('../dist/.tmp'):
    with open('../dist/.tmp/' + fname) as file:
        j = json.load(file)
        for college in j:
            college_name = college.get('collegeName')

            for class_category in college.get('collegeSubcategories'):
                subsection_name = class_category.get('classesCategory')

                for _class in class_category.get('classes'):
                    if _class.get('index') == 0:
                        continue
                    try:
                        course = database.create_course_section(
                            college_name,
                            int(fname[4:].split('_')[0]),
                            _class.get('IN'),
                            '-Q' in fname,
                            _class.get('CRN')[0],
                            _class.get('CRN')[1],
                            _class.get('CN'),
                            _class.get('SC'),
                            _class.get('IT'),
                            get_instruction_method(_class.get('IM')),
                            _class.get('SEC'),
                            _class.get('CT'),
                            create_dt_obj(_class.get('DT')),
                            float(_class.get('CR')) if _class.get('CR') else 0.0,
                            int(_class.get('MAX')) if _class.get('MAX') else 0,
                            int(_class.get('ENROLLED')) if _class.get('ENROLLED') else 0
                        )
                        course.save()
                    except ValueError as e:
                        print('CR', _class.get('CR'))
                        exit(0)
