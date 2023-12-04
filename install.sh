#!/bin/sh

echo "Coping service and executable"
cp systemd-unit/ksysguard-gpu.service /etc/systemd/system/ksysguard-gpu.service
mkdir /usr/share/ksysguard-gpu/
cp src/amd.py src/nvidia.py src/intel.py src/ksysguard-gpu.py /usr/share/ksysguard-gpu/
ln -s /usr/share/ksysguard-gpu/ksysguard-gpu.py /usr/bin/ksysguard-gpu.py
chmod +x /usr/share/ksysguard-gpu/*

echo "Enabling ksysguard-gpu in systemd"
systemctl enable --now ksysguard-gpu
