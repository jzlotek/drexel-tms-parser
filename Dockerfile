FROM python:3.7.1-stretch

RUN git clone https://github.com/jzlotek/drexel-tms-parser.git

RUN cd drexel-tms-parser

RUN pip3 install virtualenv

RUN virtualenv ./venv -p python3

EXPOSE 5000

RUN source ./venv/bin/activate

RUN pip install -r ./requirements.txt

CMD ["python", "src/app.py"]