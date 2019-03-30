FROM alpine:3.8

RUN apk --update add python3 bash perl curl wget grep sed docker sudo mysql-client postgresql-client make git
ADD . /infracheck
ADD .git /infracheck/

RUN cd /infracheck \
    && git remote remove origin || true \
    && git remote add origin https://github.com/riotkit-org/infracheck.git \
    && make install \
    && make unit_test \
    && set -x && cd /infracheck/app && ./functional-test.sh \
    && rm -rf /infracheck/.git /infracheck/example /infracheck/tests \
    && rm -rf /var/cache/apk/* \
    && chmod +x /infracheck/entrypoint.sh

ENTRYPOINT ["/infracheck/entrypoint.sh"]
