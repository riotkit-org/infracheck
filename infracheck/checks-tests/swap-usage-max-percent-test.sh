#!/bin/bash

echo " >> Assert that current usage of 50% is higher than maximum of 40%"
MOCK_SWAP_USAGE=50 MAX_ALLOWED_PERCENTAGE=40 ../checks/swap-usage-max-percent
if [[ $? != 1 ]]; then
    echo " >> Test failed."
    exit 1
fi

echo " >> Assert that swap is not used"
MOCK_SWAP_USAGE=0 MAX_ALLOWED_PERCENTAGE=0 ../checks/swap-usage-max-percent
if [[ $? != 0 ]]; then
    echo " >> Test failed."
    exit 1
fi

echo " >> Assert 10% is ok, when maximum is defined at 15%"
MOCK_SWAP_USAGE=10 MAX_ALLOWED_PERCENTAGE=15 ../checks/swap-usage-max-percent
if [[ $? != 0 ]]; then
    echo " >> Test failed."
    exit 1
fi

exit 0
