#!/bin/sh

echo "Coping service and executable"
cp gpuStatsServer.service /etc/systemd/system/gpuStatsServer.service
cp gpuServer.py /usr/bin/gpuServer.py
chmod +x /usr/bin/gpuServer.py

echo "Enabling gpuStatsServer in systemd"
systemctl enable --now gpuStatsServer
