# ksysguard-gpu
Add GPU status visualization for ksysguard.  

##### Table of Contents  
- [screnshoot](#screnshoot)
- [supported GPU](#supported-gpu)
- [dependency](#dependency)
- [installation](#installation)
- [example tab](#example-tab)
- [troubleshooting](#troubleshooting)
- [suggestion](#suggestion)
- [multiple GPU support](#multiple-gpu-support)

## screnshoot
![Example amd](images/Result.png?raw=true "example")
![Example amd and intel](images/gpu%20slacking.png?raw=true "example")

## supported GPU
AMD card are supported with [radeontop](https://github.com/clbr/radeontop)
Intel card are supported with [intel-gpu-tools](https://cgit.freedesktop.org/xorg/app/intel-gpu-tools/)  
Test those program as I had varing degree of luck on model of GPU supported and what data is exposed.  

## dependency
You need to have installed radeontop and python3 (I used 3.7), and of course ksysguard.  
Also the script will use your TCP port 3112, so you could also use it to check on remote machines, as long as you know to set up the classic firewall/nat rules.

## installation
cd ksysguard-gpu
* ./install.sh
* start ksysguard
* File -> Monitor remote machine, in the windows that will appear you will see the following:  
** Host: 127.0.0.1  
** Connection type: daemon  
** Port: 3112  
* click ok

## example tab
In the folder `tab` you can find the some example tab that can be imported into ksysguard.
Unfortunately there seems to be great difference between the data exposed by different GPU model; so you may still need to tweak here and there.

## troubleshooting
* try to run radeontop, if it works, great, close it. 
* If it does not, fix it. 
* If it require root, also check your user is part of the "video" group or whatever "ls -la /dev/dri/card0" returns.
* run the script gpuServer.py, with root/sudo if needed
* start ksysguard

![Monitor remote machine in all its glory](images/Connect%20Host.png?raw=true "Monitor remote machine")

Now if you open a new tab, in the sensor browser, you should see a new voice 127.0.0.1 with all the sensor available.  
You will notice the bus number is incuded; yep, it will work if you have multiple GPU!  
All value are % because was easier to code, deal with it.  

![The list of the sensors](images/Sensors%20List.png?raw=true "Sensor list example")

## suggestion

IMHO The most meaninful (the one in the screenshot with AMD only) are:

- gpu: estimation of the GPU usage

- vram: how much ram is in use

- mclk: memory clock
- sclk: shader clock

## multiple GPU support

radeontop is able to identify multiple GPU, by their bus number. intel-gpu-tools looks like can't do that, so if you want multiple Intel GPU will not work.. But if you take a dump of the output of `intel_gpu_top  -l` I'll see if I feel I want implement it.
