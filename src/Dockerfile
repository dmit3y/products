FROM python:3.7-alpine3.9

RUN apk -U add gcc musl-dev

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

WORKDIR /usr/src/app
ADD . /usr/src/app/
RUN chmod +x entrypoint

COPY ./loadcsv /etc/periodic/15min/loadcsv
RUN chmod +x /etc/periodic/15min/loadcsv

ENTRYPOINT ["/usr/src/app/entrypoint"]
CMD ["prepare", "python", "run.py", "runserver"]
