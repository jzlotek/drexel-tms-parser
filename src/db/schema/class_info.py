from mongoengine import StringField, IntField, FloatField, BooleanField, Document


class ClassInfo(Document):
    college = StringField(required=True)
    isQuarter = BooleanField(required=True)
    # Course Number
    cn = StringField(required=True)
    # Subject Code i.e. CS, UNIV, MATH
    # TODO: separate collections by the sc field to make lookups 
    # faster when looking for a class in a sqecific subject
    sc = StringField(required=True)
    # Instruction Type
    # Lecture, Lab & Lecture, Lab, etc
    it = StringField(required=True)
    title = StringField(required=True)
    # 0: Face to Face
    # 1: Online
    # 2: Hybrid
    # 3: Community Based Learning
    im = IntField(required=True)
    # Credits
    cr = FloatField(required=True)
