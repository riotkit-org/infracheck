FROM alpine:3.8

RUN apk --update add python3 py3-tornado py3-argparse bash perl curl wget grep sed
ADD ./app/ /app

# tests
RUN set -x && cd /app && ./test.sh

ENTRYPOINT ["/bin/bash", "-c", "cd /app && python3 ./infracheck/bin.py --server --server-port 8000"]
