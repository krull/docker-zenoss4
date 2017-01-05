#!/bin/bash
set -eo pipefail
shopt -s nullglob

echo "Starting the zenoss daemons"
service zenoss start
