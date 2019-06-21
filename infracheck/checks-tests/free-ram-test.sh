#!/bin/bash

echo " >> Assert that 2GB free (3/5GB used) is ok when max usage is 70%"
MOCK_FREE_RAM=3000 MOCK_TOTAL_RAM=5000 MAX_RAM_PERCENTAGE=70 ../checks/free-ram
[[ $? == 1 ]] && echo " .. Test failed." && exit 1
[[ $? == 127 ]] && echo " .. Test lacking a parameter." && exit 127

echo " >> Assert that 2GB free (8/10GB used) is too much when max usage is 60%"
MOCK_FREE_RAM=2000 MOCK_TOTAL_RAM=10000 MAX_RAM_PERCENTAGE=60 ../checks/free-ram
[[ $? == 0 ]] && echo " .. Test failed." && exit 0
[[ $? == 127 ]] && echo " .. Test lacking a parameter." && exit 127

echo " >> Assert that 5/10GB used is ok when max usage is 60%"
MOCK_FREE_RAM=5000 MOCK_TOTAL_RAM=10000 MAX_RAM_PERCENTAGE=60 ../checks/free-ram
[[ $? == 1 ]] && echo " .. Test failed." && exit 1
[[ $? == 127 ]] && echo " .. Test lacking a parameter." && exit 127

exit 0
