import json
import bs4
import datetime
import requests
from sdk.crawler.constants import BASE_URL


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SerializeableJSON):
            return obj.toJSON()

        return json.JSONEncoder.default(self, obj)


class SerializeableJSON:
    def toJSON(self):
        return json.dumps(self.__dict__)


class RowData(SerializeableJSON):
    def __init__(self, fields, index):
        self.row = []
        self.index = index
        fields = fields.find_all('td')
        for field in fields:
            if isinstance(field, bs4.element.Tag):
                if field.a is not None:
                    self.row.append(
                        [field.text.strip(), str(field.a.get('href'))])
                else:
                    self.row.append(field.text.strip())

    def has_data(self):
        return len(self.row) > 0 and len(self.row[0]) > 0


def to_dt(time):
    time = time.split(' ')
    am_pm = time[-1]
    try:
        hours, minutes = time[0].split(':')
    except ValueError:
        return None
    hours = int(hours)
    minutes = int(minutes)
    if am_pm.lower() == "pm" and hours != 12:
        hours += 12
    return str(datetime.time(hours, minutes if minutes < 60 else 59, 0, 0))


def get_credits(page):
    page = requests.get(page).text
    page = bs4.BeautifulSoup(page, 'html.parser')
    cred = page.find(class_="tableHeader",
                     text="Credits").parent.find(class_="even")
    cred = cred.text.strip()
    enroll = page.find(class_="tableHeader",
                       text="Enroll").parent.find(class_="odd")
    enroll = int(enroll.text.strip())
    max_enroll = page.find(class_="tableHeader",
                           text="Max Enroll").parent.find(class_="even")
    max_enroll = int(max_enroll.text.strip())
    return [cred, enroll, max_enroll]


def symboltime_to_datatime(time_range):
    time_range = time_range.split(' - ')
    time_range = list(map(to_dt, time_range))
    return time_range

def time_to_number(time):
    values = time.split(':')

    if len(values) >= 2:
        return int(values[0]) * 60 + int(values[1])
    elif len(values) == 1:
        return int(values[0]) * 60
    else:
        return 0

def create_start_end(times):
    if len(times) != 2:
        return {'start': 0, 'end': 0}
    return {'start': time_to_number(times[0]), 'end': time_to_number(times[1])}


def build_date_time_obj(days, times):
    res = {}
    if type(times) != list:
        times = symboltime_to_datatime(times)
    if days.upper() == 'TBD':
        return { 'TBD': 'TBD' }

    for day in days:
        res.update({day: create_start_end(times)})

    return res


class TMSClass(SerializeableJSON):
    def __init__(self, row):
        self.index = row.index
        self.sc = row.row[0]
        self.cn = row.row[1]
        self.it = row.row[2]
        self.im = row.row[3]
        self.sec = row.row[4]
        self.crn = row.row[5]
        if isinstance(self.crn, list) and len(self.crn) >= 2:
            self.crn[1] = (BASE_URL + self.crn[1])
        self.title = row.row[6]
        dt = row.row[7].split('\n')
        if len(dt) < 2:
            dt.append([])
        self.meeting = build_date_time_obj(dt[0], dt[1])
        self.ins = row.row[-1]
        try:
            info = get_credits(self.crn[1])
            tmp = float(info[0])
            self.maxEnroll = info[2]
            self.enrolled = info[1]
        except:
            tmp = ""

        self.cr = tmp
