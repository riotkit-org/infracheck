#!/bin/bash

echo " >> Assert will remind one day before"
REF_DATE=2019-01-10 NOW=2019-01-09 EACH=year ALERT_DAYS_BEFORE=1 ../checks/reminder
if [[ $? != 1 ]]; then
    echo " >> Test failed."
    exit 1
fi

echo " >> Assert will say there is still time - no alert raised"
REF_DATE=2019-01-10 NOW=2019-01-02 EACH=year ALERT_DAYS_BEFORE=1 ../checks/reminder
if [[ $? != 0 ]]; then
    echo " >> Test failed."
    exit 1
fi

echo " >> Assert will raise alert when there are 2 days left at YEAR CHANGE"
REF_DATE=2019-01-02 NOW=2018-12-31 EACH=year ALERT_DAYS_BEFORE=2 ../checks/reminder
if [[ $? != 1 ]]; then
    echo " >> Test failed."
    exit 1
fi

echo " >> Assert will calculate date in next year, when the event already passed (should show 334 days left)"
REF_DATE=2019-01-02 NOW=2019-01-31 EACH=year ALERT_DAYS_BEFORE=2 ../checks/reminder
if [[ $? != 0 ]]; then
    echo " >> Test failed."
    exit 1
fi

exit 0
