# ksysguard-gpu
add gpu visualization for ksysguard.

## dependency
you need to have installed radeontop and python3 (I used 3.7), and of course ksysguard.

## setup
- try to run radeontop, if it works, great, close it. 
- If it does not, fix it. 
- If it require root, also check your user is part of the "video" group or whatever "ls -la /dev/dri/card0" returns.
- run the script gpuServer.py, with root/sudo if needed
- start ksysguard
- File -> Monitor remote machine, in the windows that will appeat sewt the following:
-- Host: 127.0.0.1
-- Connection type: daemon
-- port: 3112
- click ok

now if you open a new tab, in the sensor browser, you should see a new voice 127.0.0.1 with all the sensor available. 
All value are % because was easier to code, deal with it.

The most meaninful (the one in the screenshot) IMHO are:

- gpu: estimation of the GPU usage

- vram: how much ram is in use

- mclk: memory clock
- sclk: shader clock
