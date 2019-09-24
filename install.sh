#!/bin/sh

SCRIPTLOCATION="`pwd`/gpuStatsServer.py"
echo "Updateing `pwd`/gpuStatsServer.py as location of script for gpuStatsServer.service"
sed "s,/script/location/gpuStatsServer.py,${SCRIPTLOCATION},g" ./gpuStatsServer.service.default > ./build/gpuStatsServer.service
echo "Creating sym link to gpuStatsServer.service in ${HOME}/.config/systemd/user/"
cp `pwd`/build/gpuStatsServer.service ${HOME}/.config/systemd/user/gpuStatsServer.service
echo "Changing radeontop to run for ${USER} as root without sudo"
sudo chmod u+s `which radeontop`
echo "Enabling gpuStatsServer in systemd"
systemctl enable --user gpuStatsServer --now
