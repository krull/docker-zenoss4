#!/bin/bash

set -e

echo "Starting the zenoss daemons..."
service zenoss start & tail -f /usr/local/zenoss/log/Z2.log
