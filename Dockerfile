FROM python:3.7.1-stretch

RUN git clone https://github.com/jzlotek/drexel-tms-parser.git /home/drexel-tms-parser

WORKDIR /home/drexel-tms-parser

ENV MONGO_URI mongodb+srv://admin:password1234@drexel-tms-vfw3g.mongodb.net/drexel-tms?retryWrites=true

RUN pip3 install virtualenv

RUN virtualenv ./venv -p python3

EXPOSE 5000

RUN /bin/bash -c "source ./venv/bin/activate"

RUN pip install -r ./requirements.txt

CMD ["python", "src/app.py"]