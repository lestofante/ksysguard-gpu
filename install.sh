#!/bin/sh

echo "Copying service and executable"
cp systemd-unit/ksysguard-gpu.service /etc/systemd/system/ksysguard-gpu.service
cd src
zip -r ksysguard-gpu.zip __main__.py amd.py intel.py nvidia.py ksysguard-gpu.py
cp ksysguard-gpu.zip /usr/bin/
rm ksysguard-gpu.zip

echo "Enabling ksysguard-gpu in systemd"
systemctl enable --now ksysguard-gpu

