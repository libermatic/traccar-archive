FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y percona-toolkit \
    && apt-get -y auto-remove \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt --no-cache-dir

COPY ./app /app
WORKDIR /app

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python", "main.py"]