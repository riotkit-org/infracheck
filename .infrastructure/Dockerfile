FROM alpine:3.9

RUN apk --update add python3 bash perl curl wget grep sed docker sudo mysql-client postgresql-client make git supervisor tzdata
ADD . /infracheck
ADD .git /infracheck/

ENV CHECK_INTERVAL="*/1 * * * *" \
    WAIT_TIME=0\
    LAZY=false

RUN cd /infracheck \
    # install as a package
    && git remote remove origin || true \
    && git remote add origin https://github.com/riotkit-org/infracheck.git \
    && make install \
    \
    # execute unit tests and functional tests, to make sure the application works
    && make unit_test \
    && set -x && cd /infracheck/infracheck && ./functional-test.sh \
    \
    # after installing as package extract infrastructural files
    \
    && cp -pr /infracheck/entrypoint.sh / \
    && cp -pr /infracheck/supervisord.conf /etc/supervisord.conf \
    && chmod +x /entrypoint.sh \
    \
    # delete the temporary directory after the application was installed via setuptools
    && rm -rf /infracheck \
    \
    # simple check that application does not crash at the beginning (is correctly packaged)
    && infracheck --help

ENTRYPOINT ["/entrypoint.sh"]
