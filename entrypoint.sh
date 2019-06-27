#!/bin/bash

# depending on operating system, create an entrypoint for cron
echo "#!/bin/bash" > /entrypoint.cron.sh

# check interval can be configured using environment variables
echo "${CHECK_INTERVAL} infracheck --force --wait=${WAIT_TIME}" > /etc/crontabs/root

# different base images are for x86_64 and for armv7
if which crond > /dev/null; then
    echo "crond -d 2 -f" >> /entrypoint.cron.sh
else
    echo "cron -f" >> /entrypoint.cron.sh
fi

chmod +x /entrypoint.cron.sh

ARGS=""

if [[ ${LAZY} == "true"  ]] || ${LAZY} == "1" ]]; then
    ARGS="${ARGS} --lazy "
fi

# allow to pass custom arguments from docker run command
echo "#!/bin/bash" > /entrypoint.cmd.sh
echo "infracheck --server --server-port 8000 ${ARGS} $@" >> /entrypoint.cmd.sh
chmod +x /entrypoint.cmd.sh

exec supervisord -c /infracheck/supervisord.conf
