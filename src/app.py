from flask import Flask, render_template, Response, request
import datetime
import multiprocessing
import os
from db import database
import json
from utils import Logger

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")


def query_builder(query, database):

    if query.get('subject'):
        database.subject_code(query.get('subject'))
    if query.get('section'):
        database.section(query.get('section'))
    if query.get('crn'):
        database.crn(int(query.get('crn')))
    if query.get('college'):
        database.college(query.get('college'))
    if query.get('instructor'):
        database.instructor(query.get('instructor'))
    if query.get('course_number'):
        database.course_number(query.get('course_number'))
    if query.get('instruction_method'):
        database.instruction_method(int(query.get('instruction_method')))
    if query.get('credits'):
        database.credits(float(query.get('credits')))
    if query.get('year'):
        database.year(int(query.get('year')))
    if query.get('days'):
        database.meeting(query.get('days'), 'days')


@app.route('/course', methods=['GET'])
def get_course():
    query_builder(request.args, database)

    return Response(json.dumps(database.execute()), mimetype='application/json')


if __name__ == '__main__':
    logger = Logger().logger()
    logger.info("Starting main")
    if 'dist' not in os.listdir('../'):
        logger.debug("Making dist folders")
        os.mkdir('../dist')

    if '.tmp' not in os.listdir('../dist'):
        os.mkdir('../dist/.tmp')

    try:
        app.run(host="0.0.0.0", debug=True)
    except Exception as e:
        print(e)
