FROM balenalib/armv7hf-debian:buster

ENV CHECK_INTERVAL="*/1 * * * *" \
    WAIT_TIME=0

RUN [ "cross-build-start" ]
RUN apt-get update \
    && apt-get -y install python3 python3-pip bash perl curl wget grep sed docker.io \
                          sudo mariadb-client postgresql-client netcat ca-certificates \
                          git openssl make python3-setuptools supervisor cron \
    && apt-get clean
RUN [ "cross-build-end" ]

ADD . /infracheck
ADD .git /infracheck/

RUN [ "cross-build-start" ]
RUN cd /infracheck \
    && git remote remove origin || true \
    && git remote add origin https://github.com/riotkit-org/infracheck.git \
    && make install \
    && make unit_test \
    && set -x && cd /infracheck/infracheck && ./functional-test.sh \
    && rm -rf /infracheck/.git /infracheck/example /infracheck/tests \
    && rm -rf /var/cache/apk/* \
    && chmod +x /infracheck/entrypoint.sh \
    && infracheck --help
RUN [ "cross-build-end" ]

ENTRYPOINT ["/infracheck/entrypoint.sh"]
