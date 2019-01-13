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

    @abc.abstractmethod
    def before(self, time):
        pass

    @abc.abstractmethod
    def after(self, time):
        pass

    # excecute stored query
    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def get_list(self, l, query):
        pass

    def query_builder(self, query):
        if query.get('sc'):
            self.subject_code(query.get('sc'))
        if query.get('sec'):
            self.section(query.get('sec'))
        if query.get('crn'):
            self.crn(query.get('crn'))
        if query.get('college'):
            self.college(query.get('college'))
        if query.get('in'):
            self.instructor(query.get('in'))
        if query.get('cn'):
            self.course_number(query.get('cn'))
        if query.get('im'):
            self.instruction_method(query.get('im'))
        if query.get('cr'):
            self.credits(query.get('cr'))
        if query.get('year'):
            self.year(query.get('year'))
        if query.get('days'):
            self.meeting(query.get('days'), 'days')
        if query.get('before'):
            self.before(query.get('before'))
        if query.get('after'):
            self.after(query.get('after'))

    def clear_query(self):
        self.query = dict()

    @abc.abstractmethod
    def get_query(self):
        pass
