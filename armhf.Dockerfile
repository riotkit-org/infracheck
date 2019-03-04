FROM balenalib/armv7hf-debian:buster

ADD ./app/ /app
ADD ./requirements.txt /app/
ADD ./entrypoint.sh /entrypoint.sh

RUN [ "cross-build-start" ]

RUN apt-get update \
    && apt-get install python3 python3-pip bash perl curl wget grep sed docker.io sudo mariadb-client netcat ca-certificates openssl \
    && apt-get clean \
    && pip3 install setuptools wheel --upgrade \
    && pip3 install -r /app/requirements.txt \
    && chmod +x /entrypoint.sh

# tests
RUN set -x && cd /app && ./test.sh

RUN [ "cross-build-end" ]

ENTRYPOINT ["/entrypoint.sh"]
