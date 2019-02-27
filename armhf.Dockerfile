FROM balenalib/armv7hf-alpine:3.9

ADD ./app/ /app
ADD ./entrypoint.sh /entrypoint.sh

RUN [ "cross-build-start" ]

RUN apk --update add python3 py3-tornado py3-argparse bash perl curl wget grep sed docker sudo \
    && chmod +x /entrypoint.sh

# tests
RUN set -x && cd /app && ./test.sh

RUN [ "cross-build-end" ]

ENTRYPOINT ["/entrypoint.sh"]
