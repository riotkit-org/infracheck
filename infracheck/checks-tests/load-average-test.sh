#!/bin/bash

echo " >> Assert that 1.5 core load is more than 1.0 core allowed"
MAX_LOAD=1.0 MOCK_LOAD_AVERAGE=1.5 ../checks/load-average
if [[ $? != 1 ]]; then
    echo " >> Test failed."
    exit 1
fi

echo " >> Assert that 1.5 core load is more than 1.0 core allowed (using integer instead of float)"
MAX_LOAD=1 MOCK_LOAD_AVERAGE=1.5 ../checks/load-average
if [[ $? != 1 ]]; then
    echo " >> Test failed."
    exit 1
fi

echo " >> Assert that load of 10.1 is ok, when we allow load of max. 15.0"
MAX_LOAD=15 MOCK_LOAD_AVERAGE=10.1 ../checks/load-average
if [[ $? != 0 ]]; then
    echo " >> Test failed."
    exit 1
fi

exit 0
