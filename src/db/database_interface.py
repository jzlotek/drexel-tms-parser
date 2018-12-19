import abc


class Database(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    # DB query building methods
    @abc.abstractmethod
    def year(self, year):
        pass

    @abc.abstractmethod
    def section(self, section):
        pass

    @abc.abstractmethod
    def crn(self, crn):
        pass

    @abc.abstractmethod
    def meeting(self, meeting, type_):
        pass

    @abc.abstractmethod
    def instructor(self, instructor):
        pass

    @abc.abstractmethod
    def college(self, college):
        pass

    @abc.abstractmethod
    def course_number(self, cn):
        pass

    @abc.abstractmethod
    def subject_code(self, sc):
        pass

    @abc.abstractmethod
    def instruction_type(self, it):
        pass

    @abc.abstractmethod
    def instruction_method(self, im):
        pass

    @abc.abstractmethod
    def credits(self, cr):
        pass

    # excecute stored query
    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def get_query(self):
        pass
