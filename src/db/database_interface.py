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

    def query_builder(self, query):
        if query.get('subject'):
            self.subject_code(query.get('subject'))
        if query.get('section'):
            self.section(query.get('section'))
        if query.get('crn'):
            self.crn(query.get('crn'))
        if query.get('college'):
            self.college(query.get('college'))
        if query.get('instructor'):
            self.instructor(query.get('instructor'))
        if query.get('course_number'):
            self.course_number(query.get('course_number'))
        if query.get('instruction_method'):
            self.instruction_method(query.get('instruction_method'))
        if query.get('credits'):
            self.credits(query.get('credits'))
        if query.get('year'):
            self.year(query.get('year'))
        if query.get('days'):
            self.meeting(query.get('days'), 'days')

    @abc.abstractmethod
    def get_query(self):
        pass
