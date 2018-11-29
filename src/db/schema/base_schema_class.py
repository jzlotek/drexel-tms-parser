from mongoengine import Document
import abc


class BaseSchema(Document, abc.ABC):
    pass
