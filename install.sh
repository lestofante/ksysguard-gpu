#!/bin/sh

echo "Coping service and executable"
cp systemd-unit/gpuStatsServer.service /etc/systemd/system/gpuStatsServer.service
cp src/gpuStatsServer.py /usr/bin/
chmod +x /usr/bin/gpuStatsServer.py

echo "Enabling gpuStatsServer in systemd"
systemctl enable --now gpuStatsServer
