FROM python:3.7.1-stretch

ARG PORT

ARG SERVLET
ENV SERVLET=$SERVLET

RUN git clone https://github.com/jzlotek/drexel-tms-parser.git /home/drexel-tms-parser

WORKDIR /home/drexel-tms-parser

RUN pip3 install virtualenv

RUN virtualenv ./venv -p python3

RUN /bin/bash -c "source ./venv/bin/activate"

RUN pip install -r ./requirements.txt

EXPOSE $PORT

CMD ["/bin/bash", "-c", "python src/${SERVLET}"]