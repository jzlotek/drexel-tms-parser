FROM node:10.15.0-stretch

RUN git clone https://github.com/jzlotek/drexel-tms-parser.git /home/drexel-tms-parser
WORKDIR /home/drexel-tms-parser

RUN git checkout heroku

ARG NODE_CMD=''
RUN npm install -g yarn
RUN /bin/bash -c "if [[ '${NODE_CMD}' != '' ]]; then /bin/bash -c ${NODE_CMD}; fi"

# setting up servlet config
FROM python:3.7.1-stretch

ARG PORT
ARG SERVLET=4000
ENV SERVLET=$SERVLET

RUN pip3 install virtualenv

RUN virtualenv ./venv -p python3

RUN /bin/bash -c "source ./venv/bin/activate"

RUN pip install -r ./requirements.txt

EXPOSE $PORT

CMD ["/bin/bash", "-c", "python src/${SERVLET}"]