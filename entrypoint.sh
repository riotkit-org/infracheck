#!/bin/bash

cd /app
exec python3 ./infracheck/bin.py --server --server-port 8000 $@
