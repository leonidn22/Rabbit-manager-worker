#!/usr/bin/env bash

# go to working dir
PROGDIR=`dirname $0`
cd $PROGDIR

PYTHON_BIN="python3.7"


${PYTHON_BIN} manager.py &

${PYTHON_BIN} worker.py &

