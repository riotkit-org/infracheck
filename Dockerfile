FROM alpine:3.8

RUN apk --update add python3 py3-tornado py3-argparse bash perl curl wget grep sed docker sudo
ADD ./app/ /app
ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# tests
RUN set -x && cd /app && ./test.sh

ENTRYPOINT ["/entrypoint.sh"]
