FROM python:3.7.2-stretch as python-build
WORKDIR /home/drexel-tms-parser

RUN pip3 install virtualenv

RUN virtualenv ./venv -p python3

RUN /bin/bash -c "source ./venv/bin/activate"

COPY requirements.txt /home/drexel-tms-parser
RUN pip3 install -r ./requirements.txt

# BEGIN NPM installation
COPY --from=python-build /home/drexel-tms-parser /home/drexel-tms-parser
COPY . /home/drexel-tms-parser

ARG NODE_CMD=''
ENV NODE_CMD=$NODE_CMD
RUN /bin/bash -c "if [[ '${NODE_CMD}' != '' ]]; then curl -sL https://deb.nodesource.com/setup_10.x | bash - && apt-get install -y nodejs; fi"

# setting up servlet config

ARG PORT=4000
ENV PORT=$PORT
ARG SERVLET=''
ENV SERVLET=$SERVLET


EXPOSE $PORT

CMD ["/bin/bash", "-c", "if [[ '${NODE_CMD}' != '' ]]; then /bin/bash -c 'npm install && npm rebuild node-sass && ${NODE_CMD}'; fi; python src/${SERVLET}"]
