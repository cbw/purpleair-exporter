#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
SETUP_FILE="$SCRIPT_DIR/../setup.py"

grep VERSION $SETUP_FILE | awk -F"= " '{print $2}' | tr -d '"'
