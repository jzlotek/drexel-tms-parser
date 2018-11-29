from db.schema.base_schema_class import BaseSchema
from mongoengine import ListField, StringField, DateField, IntField, FloatField


class Section(BaseSchema):
    crn = IntField(required=True)
