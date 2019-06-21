#!/bin/bash

echo " >> Assert that 3,2GB is not enough, 4GB at least required"
MOCK_FREE_SPACE="3.2" DIR=/ MIN_REQ_SPACE=4 ../checks/disk-space
[[ "$?" == 0 ]] && echo " .. Test failed." && exit 1

echo " >> Assert 4.5GB is enough, when minimum is 4GB"
MOCK_FREE_SPACE="4.5" DIR=/ MIN_REQ_SPACE=4 ../checks/disk-space
[[ "$?" == 1 ]] && echo " .. Test failed." && exit 1

echo " >> Assert 50GB is enough, when minimum is 10GB"
MOCK_FREE_SPACE="50" DIR=/ MIN_REQ_SPACE=10 ../checks/disk-space
[[ "$?" == 1 ]] && echo " .. Test failed." && exit 1

exit 0
