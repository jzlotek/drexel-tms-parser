from mongoengine import ListField, StringField, DateField, IntField, FloatField, DictField, Document


class Section(Document):
    crn = IntField(required=True)
    crnLink = StringField(required=True)
    # Course Number
    cn = IntField(required=True)
    # Subject Code i.e. CS, UNIV, MATH
    # TODO: separate collections by the sc field to make lookups 
    # faster when looking for a class in a sqecific subject
    sc = StringField(required=True)
    # Instruction Type
    # Lecture, Lab & Lecture, Lab, etc
    it = StringField(required=True)
    # 0: Face to Face
    # 1: Online
    # 2: Hybrid
    # 3: Community Based Learning
    im = IntField(required=True)
    # Section i.e. 001, 002, A, B
    sec = StringField(required=True)
    title = StringField(required=True)
    meeting = DictField(required=True)
    # Credits
    cr = FloatField(required=True)
    instructor = StringField(required=True)
    maxEnroll = IntField(required=True)
    enrolled = IntField(required=True)



