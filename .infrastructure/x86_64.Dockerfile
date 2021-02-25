FROM alpine:3.12

RUN apk --update add python3 bash perl curl wget grep sed docker sudo mysql-client postgresql-client git tzdata \
                     sshpass openssh-client
ADD . /infracheck
ADD .git /infracheck/
ADD .infrastructure /infracheck/

ENV REFRESH_TIME="120" \
    WAIT_TIME="0" \
    CHECK_TIMEOUT="10"

RUN cd /infracheck \
    && export CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
    # install as a package
    && git remote remove origin || true \
    && git remote add origin https://github.com/riotkit-org/infracheck.git \
    \
    && apk add --no-cache --update py3-pip \
    && apk add --no-cache --update --virtual BUILD_DEPS gcc python3-dev musl-dev linux-headers postgresql-dev libffi-dev \
    && pip3 install pbr==5.4.5 \
    && pip3 install -r /infracheck/requirements.txt \
    && rkd :install \
    \
    # delete the temporary directory after the application was installed via setuptools
    && rm -rf /infracheck \
    \
    # simple check that application does not crash at the beginning (is correctly packaged)
    && infracheck --help \
    \
    && apk del BUILD_DEPS

ADD /.infrastructure/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
