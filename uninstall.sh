#!/bin/sh

echo "Disabling ksysguard-gpu in systemd"
systemctl disable ksysguard-gpu
systemctl stop ksysguard-gpu

echo "Deleting service and executable"
rm /etc/systemd/system/ksysguard-gpu.service
rm /usr/bin/ksysguard-gpu.py
rm -r /usr/share/ksysguard-gpu


