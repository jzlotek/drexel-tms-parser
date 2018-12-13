FROM python:3.7.1-stretch

RUN git clone https://github.com/jzlotek/drexel-tms-parser.git /home/drexel-tms-parser

WORKDIR /home/drexel-tms-parser

RUN pip3 install virtualenv

RUN virtualenv ./venv -p python3

RUN /bin/bash -c "source ./venv/bin/activate"

RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD ["python", "src/app.py"]