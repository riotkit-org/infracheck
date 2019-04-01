#!/bin/bash

# depending on operating system, create an entrypoint for cron
echo "#!/bin/bash" > /entrypoint.cron.sh

if which crond > /dev/null; then
    echo "crond -d 2 -f" >> /entrypoint.cron.sh
else
    echo "cron -f" >> /entrypoint.cron.sh
fi

chmod +x /entrypoint.cron.sh

# allow to pass custom arguments from docker run command
echo "#!/bin/bash" > /entrypoint.cmd.sh
echo "infracheck --server --server-port 8000 $@" >> /entrypoint.cmd.sh
chmod +x /entrypoint.cmd.sh

if [[ "${CHECK_INTERVAL}" != "" ]]; then
    echo "${CHECK_INTERVAL} infracheck" > /etc/crontabs/root
fi

exec supervisord -c /infracheck/supervisord.conf
