#!/bin/bash

cd /
exec infracheck --server --server-port 8000 $@
