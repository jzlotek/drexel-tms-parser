from mongoengine import StringField, IntField, DictField, Document


class Section(Document):
    course = StringField(required=True)
    year = IntField(required=True)
    semester = StringField(required=True)
    crn = IntField(required=True)
    crnLink = StringField(required=True)
    # Section i.e. 001, 002, A, B
    sec = StringField(required=True)
    meeting = DictField(required=True)
    instructor = StringField(required=True)
    maxEnroll = IntField(required=True)
    enrolled = IntField(required=True)



