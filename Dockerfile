FROM python:3.10-alpine

RUN set -x \
    && apk add --update perl perl-dbi perl-dbd-mysql \
    && wget -O /tmp/pt-archiver https://percona.com/get/pt-archiver \
    && install /tmp/pt-archiver /usr/bin/pt-archiver \
    && rm -rf /var/cache/apk/* /tmp/pt-archiver

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY ./app /app
WORKDIR /app

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python", "main.py"]