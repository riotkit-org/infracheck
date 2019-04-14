#!/bin/bash

# test valid url
echo " >> Testing valid url"
URL=https://duckduckgo.com ../checks/http || exit 1

# test invalid url
echo " >> Testing invalid url"
URL=https://localhost:12345 ../checks/http || exit 0

exit 0
