#!/bin/sh

set -e

if [ -f "/opt/munki/python" ]; then
    /bin/rm /opt/munki/python
fi

if [ -d "/opt/munki/Python.framework/Versions/3.7" ]; then
    /bin/rm -r /opt/munki/Python.framework/Versions/3.7
fi

if [ -d "/opt/munki/Python.framework/Versions/3.8" ]; then
    /bin/rm -r /opt/munki/Python.framework/Versions/3.8
fi

