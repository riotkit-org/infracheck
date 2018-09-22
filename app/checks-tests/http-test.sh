#!/bin/sh

# test valid url
URL=https://google.com ../checks/http || exit 1

# test invalid url
URL=https://localhost:12345 ../checks/http || exit 0

exit 0
