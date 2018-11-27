import json
import bs4
import datetime
import requests
from crawler.constants import BASE_URL


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
        field = fields.find('td')
        while field is not None:
            if isinstance(field, bs4.element.Tag):
                if field.a is not None:
                    self.row.append([field.text.strip(), str(field.a.get('href'))])
                else:
                    self.row.append(field.text.strip())

            field = field.next_sibling

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
    if am_pm in "PMpmPmpM" and hours != 12:
        hours += 12
    return str(datetime.time(hours, minutes if minutes < 60 else 59, 0, 0))


def get_credits(page):
    page = requests.get(page).text
    page = bs4.BeautifulSoup(page, 'html.parser')
    cred = page.find(class_ = "tableHeader", text="Credits").parent.find(class_ = "even")
    cred = cred.text.strip()
    enroll = page.find(class_ = "tableHeader", text="Enroll").parent.find(class_ = "odd")
    enroll = int(enroll.text.strip())
    max_enroll = page.find(class_ = "tableHeader", text="Max Enroll").parent.find(class_ = "even")
    max_enroll = int(max_enroll.text.strip())
    return [cred, enroll, max_enroll]


def symboltime_to_datatime(time_range):
    time_range = time_range.split(' - ')
    time_range = list(map(to_dt, time_range))
    return time_range


class TMSClass(SerializeableJSON):
    def __init__(self, row):
        self.index = row.index
        self.SC = row.row[0]
        self.CN = row.row[1]
        self.IT = row.row[2]
        self.IM = row.row[3]
        self.SEC = row.row[4]
        self.CRN = row.row[5]
        if isinstance(self.CRN, list) and len(self.CRN) >= 2:
            self.CRN[1] = (BASE_URL + self.CRN[1])
        self.CT = row.row[6]
        dt = row.row[7].split('\n')
        if len(dt) > 1:
            dt[1] = symboltime_to_datatime(dt[1])
            self.DT = dict(
                days=dt[0],
                times=dt[1]
            )
        else:
            self.DT = dt
        self.IN = row.row[8]
        try:
            info = get_credits(self.CRN[1])
            tmp = float(info[0])
            self.MAX = info[2]
            self.ENROLLED = info[1]
        except:
            tmp = ""

        self.CR = tmp
