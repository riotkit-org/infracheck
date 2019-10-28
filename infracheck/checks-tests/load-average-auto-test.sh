#!/bin/bash

echo " >> Assert that load 11.6 is higher than 10+1"
MAXIMUM_ABOVE=1.0 MOCK_CPU_COUNT=10 MOCK_LOAD_AVERAGE=11.6 ../checks/load-average-auto
if [[ $? != 1 ]]; then
    echo " >> Test failed."
    exit 1
fi

echo " >> Assert that load 20 is ok, when we have 30 cores and MAXIMUM_ABOVE=0.5"
MAXIMUM_ABOVE=0.5 MOCK_CPU_COUNT=20 MOCK_LOAD_AVERAGE=20 ../checks/load-average-auto
if [[ $? != 0 ]]; then
    echo " >> Test failed."
    exit 1
fi

exit 0
