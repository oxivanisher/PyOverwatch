#!/bin/bash

# Getting script directory.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Saving origin path.
ORIGDIR=$(pwd)

# Cleaning old .pyc files to not run into the "importing seems to work" trap again!
find ${DIR} -name "*.pyc" -exec rm {} \;

# Changing to the root path of th application.
cd ${DIR}

# Checking if PYOVERWATCH_CFG is set. If not, use the provided example file.
if [ -z "$PYOVERWATCH_CFG" ]; then
	if [ -f "dist/pyoverwatch.cfg" ]; then
		echo "Setting PYOVERWATCH_CFG for you. Please use your own settings for production!"
		export PYOVERWATCH_CFG="../dist/pyoverwatch.cfg"
	else
		export PYOVERWATCH_CFG="../dist/pyoverwatch.cfg.example"
	fi
fi

# Actually starting the application.
python pyoverwatch.py

# Changing back to origin path.
cd ${ORIGDIR}