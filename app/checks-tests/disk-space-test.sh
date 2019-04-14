#!/bin/bash

echo " >> Assert that 3,2GB is not enough, 4GB at least required"
MOCK_DF_OUTPUT="3,2GB" DIR=/ MIN_REQ_SPACE=4 ../checks/disk-space
[[ "$?" == 0 ]] && echo " .. Test failed." && exit 1

echo " >> Assert 4GB is enough, when minimum is 4.5GB"
MOCK_DF_OUTPUT="4GB" DIR=/ MIN_REQ_SPACE=4.5 ../checks/disk-space
[[ "$?" == 1 ]] && echo " .. Test failed." && exit 1

echo " >> Assert 5GB is enough, when minimum is 10GB"
MOCK_DF_OUTPUT="5GB" DIR=/ MIN_REQ_SPACE=10 ../checks/disk-space
[[ "$?" == 1 ]] && echo " .. Test failed." && exit 1

exit 0
