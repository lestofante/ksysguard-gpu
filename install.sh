#!/bin/sh

echo "Copying service and executable"
cp systemd-unit/ksysguard-gpu.service /etc/systemd/system/ksysguard-gpu.service
cp src/ksysguard-gpu.py /usr/bin/
chmod +x /usr/bin/ksysguard-gpu.py

echo "Enabling ksysguard-gpu in systemd"
systemctl enable --now ksysguard-gpu
