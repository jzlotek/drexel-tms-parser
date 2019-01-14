import abc


class Database(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    # DB query building methods
    @abc.abstractmethod
    def year(self, year, query):
        pass

    @abc.abstractmethod
    def section(self, section, query):
        pass

    @abc.abstractmethod
    def crn(self, crn, query):
        pass

    @abc.abstractmethod
    def meeting(self, meeting, type_, query):
        pass

    @abc.abstractmethod
    def instructor(self, instructor, query):
        pass

    @abc.abstractmethod
    def college(self, college, query):
        pass

    @abc.abstractmethod
    def course_number(self, cn, query):
        pass

    @abc.abstractmethod
    def subject_code(self, sc, query):
        pass

    @abc.abstractmethod
    def instruction_type(self, it, query):
        pass

    @abc.abstractmethod
    def instruction_method(self, im, query):
        pass

    @abc.abstractmethod
    def credits(self, cr, query):
        pass
    
    @abc.abstractmethod
    def semester(self, semester, query):
        pass

    @abc.abstractmethod
    def before(self, time, query):
        pass

    @abc.abstractmethod
    def after(self, time, query):
        pass

    # excecute stored query
    @abc.abstractmethod
    def execute(self, query):
        pass

    @abc.abstractmethod
    def get_list(self, l, query):
        pass

    def query_builder(self, q, query):
        if q.get('sc'):
            self.subject_code(q.get('sc'), query)
        if q.get('semester'):
            self.semester(q.get('semester'), query)
        if q.get('sec'):
            self.section(q.get('sec'), query)
        if q.get('crn'):
            self.crn(q.get('crn'), query)
        if q.get('college'):
            self.college(q.get('college'), query)
        if q.get('in'):
            self.instructor(q.get('in'), query)
        if q.get('cn'):
            self.course_number(q.get('cn'), query)
        if q.get('im'):
            self.instruction_method(q.get('im'), query)
        if q.get('cr'):
            self.credits(q.get('cr'), query)
        if q.get('year'):
            self.year(q.get('year'), query)
        if q.get('days'):
            self.meeting(q.get('days'), 'days', query)
        if q.get('before'):
            self.before(q.get('before'), query)
        if q.get('after'):
            self.after(q.get('after'), query)

    def clear_query(self):
        self.query = dict()

    @abc.abstractmethod
    def get_query(self):
        pass
