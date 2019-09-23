# ksysguard-gpu
Add gpu visualization for ksysguard.  
For now, only AMD card with radeontop are supported, see https://github.com/clbr/radeontop for more info. 

![Example](Result.png?raw=true "example")

## dependency
You need to have installed radeontop and python3 (I used 3.7), and of course ksysguard.  
Also the script will use your TCP port 3112, so you could also use it to check on remote machines, as long as you know to set up the classic firewall/nat rules.

## setup
* try to run radeontop, if it works, great, close it. 
* If it does not, fix it. 
* If it require root, also check your user is part of the "video" group or whatever "ls -la /dev/dri/card0" returns.
* run the script gpuServer.py, with root/sudo if needed
* start ksysguard
* File -> Monitor remote machine, in the windows that will appeat sewt the following:  
** Host: 127.0.0.1  
** Connection type: daemon  
** Port: 3112  
* click ok

![Monitor remote machine in all its glory](Connect%20Host.png?raw=true "Monitor remote machine")

Now if you open a new tab, in the sensor browser, you should see a new voice 127.0.0.1 with all the sensor available.  
You will notice the bus number is incuded; yep, it will work if you have multiple GPU!  
All value are % because was easier to code, deal with it.  

![The list of the sensors](Sensors%20List.png?raw=true "Sensor list example")

## suggestion

IMHO The most meaninful (the one in the screenshot) are:

- gpu: estimation of the GPU usage

- vram: how much ram is in use

- mclk: memory clock
- sclk: shader clock
