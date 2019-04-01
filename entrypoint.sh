#!/bin/bash

# allow to pass custom arguments from docker run command
echo "#!/bin/bash" > /entrypoint.cmd.sh
echo "infracheck --server --server-port 8000 $@" >> /entrypoint.cmd.sh
chmod +x /entrypoint.cmd.sh

if [[ "${CHECK_INTERVAL}" != "" ]]; then
    echo "${CHECK_INTERVAL} infracheck" > /etc/crontabs/root
fi

exec supervisord -c /infracheck/supervisord.conf
