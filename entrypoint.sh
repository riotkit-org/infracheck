#!/bin/bash

CHECK_INTERVAL=$(echo "${CHECK_INTERVAL}" | sed "s/\"//g")

get_common_args () {
    echo " --directory=/data --db-path=/database/db.sqlite3 "
}

prepare_data_directory () {
    #
    # Database is outside of "data" directory, as the database contains dynamic data, that could be considered
    # as a temporary things (the cache etc.). The "data" contains configuration.
    #

    mkdir -p /database /data
    touch /database/db.sqlite3
}

prepare_crontab () {
    # depending on operating system, create an entrypoint for cron
    echo "#!/bin/bash" > /entrypoint.cron.sh

    # check interval can be configured using environment variables
    echo "${CHECK_INTERVAL} infracheck --force --wait=${WAIT_TIME} $(get_common_args) " > /etc/crontabs/root

    # different base images are for x86_64 and for armv7
    if which crond > /dev/null; then
        echo "crond -d 2 -f" >> /entrypoint.cron.sh
    else
        echo "cron -f" >> /entrypoint.cron.sh
    fi

    chmod +x /entrypoint.cron.sh
}

prepare_entrypoint () {
    ARGS=""

    if [[ ${LAZY} == "true"  ]] || ${LAZY} == "1" ]]; then
        ARGS="${ARGS} --lazy "
    fi

    # allow to pass custom arguments from docker run command
    echo "#!/bin/bash" > /entrypoint.cmd.sh
    echo "infracheck --server --server-port 8000 ${ARGS} $(get_common_args) $@" >> /entrypoint.cmd.sh

    cat /entrypoint.cmd.sh
    chmod +x /entrypoint.cmd.sh
}

prepare_data_directory
prepare_crontab
prepare_entrypoint "$@"

exec supervisord -c /etc/supervisord.conf
