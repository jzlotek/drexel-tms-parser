import requests
import bs4
import json
import threading
from sdk.crawler.constants import BASE_URL, GREEN, RESET, BOLD, BLUE, RED, CYAN
from sdk.crawler.utility import RowData, TMSClass, Encoder
from utils import logger
import multiprocessing
import time


def get_page(page, meta="", retries=3):
    for _ in range(retries):
        try:
            response = requests.get(page, timeout=
                (
                    len(multiprocessing.process.active_children()) * 60 
                    if len(multiprocessing.process.active_children()) > 1 
                    else 60
                )
            )
        except:
            continue

        if response.status_code == 200:
            logger.info('Process: {}, Thread: {}\t{blue}{bold}{}s elapsed {reset}{green}{}{reset}'
                        .format(
                            multiprocessing.process.current_process().pid,
                            hex(threading.current_thread().ident),
                            response.elapsed.total_seconds(),
                            meta,
                            green=GREEN,
                            reset=RESET,
                            bold=BOLD,
                            blue=BLUE,
                            red=RED
                        ))
            try:
                return bs4.BeautifulSoup(response.text, 'html.parser')
            except:
                return None
        else:
            logger.error('\nLink: {}\nStatus code: {}\n'.format(
                page, response.status_code))

    logger.critical(
        '\nLink: {}\nFailed after {} tries\n'.format(page, retries))
    return None


def get_college_page_sublinks(page):
    sublinks = []
    table = page.find('table', class_="collegePanel")
    if table is None:
        return []

    for child in table.children:
        if isinstance(child, bs4.element.Tag) and child.find('div'):
            divs = child.find_all('div')

            for div in divs:
                anchor = div.find('a')
                if isinstance(anchor, bs4.element.Tag):
                    sublinks.append((anchor.text, anchor.get('href')))

    return sublinks


def get_classes_on_college(page):
    classes = []

    sublinks = get_college_page_sublinks(page)
    for title, link in sublinks:
        c = get_classes_on_page(link, title)
        classes.append(
            dict(
                classesCategory=title,
                classes=c
            )
        )
    return classes


def get_classes_on_page(page, title):
    soup = get_page(BASE_URL + page, meta='{} '.format(title))

    if soup is None:
        return []

    child_tags = []

    i = 0
    for child in soup.find('tr', class_="tableHeader").parent.children:
        if isinstance(child, bs4.element.Tag):
            data = RowData(child, i)
            child_tags.append(data)
            i += 1

    child_tags = [json.loads(TMSClass(row).toJSON()) for row in child_tags if row.has_data()]

    return child_tags


def get_colleges_thread_runner(classes, class_list):
    tmp_list = []
    for c in classes:
        page_url = c[1]
        class_section = c[0]
        try:
            college_page = get_page(
                BASE_URL + page_url, meta='{} '.format(class_section))
        except:
            continue

        tmp_list.append(
            dict(
                collegeName=class_section,
                collegeSubcategories=get_classes_on_college(college_page)
            )
        )

    lock = threading.Lock()
    lock.acquire(True)
    class_list.extend(tmp_list)
    lock.release()


def get_colleges_runner(page_url, class_section, class_list):
    college_page = get_page(BASE_URL + page_url,
                            meta='{} '.format(class_section))

    class_list.append(
        dict(
            collegeName=class_section,
            collegeSubcategories=get_classes_on_college(college_page)
        )
    )


def get_colleges_from_side_left(page, threaded=False, num_threads=5):

    threads = []
    class_list = []

    colleges = page.find(id='sideLeft')
    if colleges is not None:
        colleges = colleges.find_all('a')

    colleges = [[college.text, college.get('href')]
                for college in colleges if college is not None]

    if threaded:
        college_list = [[] for _ in range(num_threads)]
        college_list_len = len(college_list)
        for x, element in enumerate(colleges):
            college_list[x % college_list_len].append(element)

        for college_sublist in college_list:
            threads.append(threading.Thread(target=get_colleges_thread_runner,
                                            args=(college_sublist, class_list)))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    else:
        for college in colleges:
            get_colleges_runner(college[1], college[0], class_list)

    return class_list


def get_links_to_terms(page):
    ret = []
    links = page.find_all('div', class_='term')
    for link in links:
        l = link.find('a')
        ret.append([l.text, l.get('href')])

    return ret


def run_on_page(quarter):
    quarter[0] = "".join(quarter[0]
                         .replace('-', '_')
                         .replace('Quarter', '-Q')
                         .replace('Semester', '-S')
                         .replace('Fall', 'Fa')
                         .replace('Winter', 'Wi')
                         .replace('Spring', 'Sp')
                         .replace('Summer', 'Su')
                         .split(' ')
                         )

    page = get_page(
        BASE_URL + quarter[1], meta='Process: {}\t{cyan}{}: '.format(multiprocessing.process.current_process().pid, quarter[0], cyan=CYAN)
    )

    if page is None:
        return

    all_classes = get_colleges_from_side_left(page, threaded=True)
    # with open(quarter[0]+ '.json', 'w') as f:
    #     f.writelines(json.dumps(all_classes, cls=Encoder))
    requests.post('http://drexel-tms-ingest:5001/ingest', json=dict(
        data=json.dumps(all_classes, cls=Encoder),
        name=quarter[0]
    ))

    return


class Crawler:
    def __init__(self, mp=False):
        logger.debug("Created crawler: {}".format(str(self)))
        self.quarters = []
        self.multiprocessing = mp
        self.update()

    def update(self):
        page = get_page('https://termmasterschedule.drexel.edu/webtms_du/app',
                        meta='{red}webTMS Homepage Init {reset}'.format(red=RED,
                                                                        reset=RESET))
        self.quarters = get_links_to_terms(page)

    def crawl(self):

        while True:
            logger.info('Starting to crawl pages')

            if self.multiprocessing:
                processes = []
                # spin a process for each semester that is to be parsed
                for quarter in self.quarters:
                    try:
                        process = multiprocessing.Process(target=run_on_page, args=(quarter,))
                        processes.append(process)
                    except:
                        pass
                for process in processes:
                    process.start()
                for process in processes:
                    process.join()
            else:
                try:
                    for quarter in self.quarters:
                        run_on_page(quarter)
                except:
                    pass
            logger.info('Done. Sleeping')
            time.sleep(60 * 60 * 24)
            # with open('./.tmp/{}.json'.format(quarter[0]), 'w') as _file:
            # _file.write(json.dumps(all_classes, cls=Encoder, indent=4))
