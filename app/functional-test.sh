#!/bin/bash

pwd=$(pwd)

for check in $(ls ./checks-tests); do
    cd ${pwd}/checks-tests

    if ! ./${check}; then
        echo ""
        echo " !!! ${check} failed"
        echo ""
        exit 1
    fi
done

exit 0
