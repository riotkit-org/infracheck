#!/bin/bash

prepare_data_directory () {
    #
    # Database is outside of "data" directory, as the database contains dynamic data, that could be considered
    # as a temporary things (the cache etc.). The "data" contains configuration.
    #

    mkdir -p /database /data
    touch /database/db.sqlite3
}

prepare_entrypoint () {
    ARGS=""

    if [[ ${REFRESH_TIME} ]]; then
        ARGS="${ARGS} --refresh-time=${REFRESH_TIME} "
    fi

    if [[ ${CHECK_TIMEOUT} ]]; then
        ARGS="${ARGS} --timeout=${CHECK_TIMEOUT} "
    fi

    if [[ ${WAIT_TIME} ]]; then
        ARGS="${ARGS} --wait=${WAIT_TIME} "
    fi

    # allow to pass custom arguments from docker run command
    echo "infracheck --server-port 8000 ${ARGS} --directory=/data --db-path=/database/db.sqlite3 $@"
}

prepare_data_directory
exec $(prepare_entrypoint "$@")
