#!/bin/sh

echo "clearing the build dir"
rm ./build/*
echo "Stoping service and removing from systemd" 
systemctl --user disable gpuStatsServer --now
echo "Removing gpuStatsServer.service from ${HOME}/.config/systemd/user/"
rm ${HOME}/.config/systemd/user/gpuStatsServer.service
