#!/bin/bash
#
# Merciless uninstall of munki.

if [ `id -u` -ne 0 ]; then
    echo "Munki uninstallation must be run by root"
    exit 1
fi

launchctl unload /Library/LaunchDaemons/dev.andre4ik3.managed.munki.*
rm -rf '/Applications/Utilities/Managed Software Update.app'
rm -rf '/Applications/Managed Software Center.app'
rm -f /Library/LaunchDaemons/dev.andre4ik3.managed.munki.*
rm -f /Library/LaunchAgents/dev.andre4ik3.managed.munki.*
rm -rf '/Library/Managed Installs'
rm -rf /opt/munki
pkgutil --forget dev.andre4ik3.managed.munki.core
pkgutil --forget dev.andre4ik3.managed.munki.admin
pkgutil --forget dev.andre4ik3.managed.munki.app
pkgutil --forget dev.andre4ik3.managed.munki.launchd
pkgutil --forget dev.andre4ik3.managed.munki.app_status
pkgutil --forget dev.andre4ik3.managed.munki
