# Jacky Printo

## Overview

This is a simple interface to a set of ender3 stages and the Ultimus V dispenser. It provides 

- A simple keyboard based control to position the syringe tip
- A basic set of interfaces to send
    - GCode directly to the ender3
    - Serial commands to the Ultimus V
- It also interfaces with uStreamer to display the syringe tip
- Finally, it exposes a basic API to allow for control via http class
    - And there’s simple python wrapper for these calls.

## Interface

![Untitled](Jacky%20Printo%20c9fa6f46cd034f869b3bac0427ab75c1/Untitled.png)

| Control/Display | What It Does | Keyboard Shortcut |
| --- | --- | --- |
| move x/y | The step size to move in x/y with a step command |  |
| x- / x+ / y- / x+ | Step the stage in x/y by move x/y | ← → ↑ ↓ |
| move z | the step size to move in z with a step command |  |
| z+ / z- | Step the stage in z by move z | w (up) s (down) |
| X/Y/Z | Current Position in X/Y/Z |  |
| B actual | Actual Bed Temperature (˚C) |  |
| B set | Confirmed Setpoint for Bed (˚C) |  |

### Dispenser Settings

| Control/Display | What It Does | Keyboard Shortcut |
| --- | --- | --- |
| Set Pressure | Set Pressure (PSI) |  |
| Set Dispense Time | Set dispense time in seconds with up to ms precision |  |
| Set Vacuum | Set Pressure (Torr) |  |
| Toggle Pressure | Fire the goop (fire ready needs to be checked) | g (only) |
| Any Command | Type the command on the line per the ‣ manu |  |

### Picture Settings

| Control/Display | What It Does | Keyboard Shortcut |
| --- | --- | --- |
| prefix | the prefix for the file name. X_Y_Z_Time is appended automatically (i.e. no overwrites are possible) |  |
| user | Your initials |  |
| 📸 | Take a snap | c |
| Camera Controls | Camera Specific settings autogenerated. Futz with to improve image quality. Won’t focus an unfocussed image |  |

## Absolute Position

| Control/Display | What It Does | Keyboard Shortcut |
| --- | --- | --- |
| Absolute Position | Set X/Y/Z specifically. Hit go to move. Hit zero to set current position to zero. |  |

### Ender Settings

| Control/Display | What It Does | Keyboard Shortcut |
| --- | --- | --- |
| Send Command | Send Marlin GCodes Directly to Ender |  |

## Python Library

Current @ [http://jackyprinto.local:8001/libjackyprinto](http://jackyprinto.local:8001/libjackyprinto) 

```python
`jackyprinto(project='test', prefix='snap', user='user', url='http://localhost', ender_port='3000', ultimus_port='9001', notes=None, practice=False)`
:   Instantiate jackyprinto instance

    ### Methods

    `get_position(self)`
    :   Get Position

    `get_snapshot(self)`
    :   Take a snapshot

    `get_snapshot_old(self, base='files', pat='snap', meta='')`
    :   [DEPRECATED] Take a snapshot

    `get_v4l2_ctls(self, values_only=False)`
    :   Get V4L2 states

    `move(self, x, y, z, absolute=False)`
    :   Move relative to x/y/z, unless absolute flag is ticked
        If None is specified don't change that position

    `send_to_dispenser(self, cmd)`
    :   Send download commands to printer

    `send_to_stage(self, cmd)`
    :   Send Marlin GCode Commands to Ender Stages

    `setDispenseTime(self, dispensetime)`
    :   Set Dispense Time (s)

    `setPressure(self, pressure)`
    :   Set Pressure (PSI)

    `setVacuum(self, dispensetime)`
    :   Set Vacuum (Torr)

    `steppers_off(self)`
    :   Turn off stepper motors

    `togglePressure(self)`
    :   Fire dispenser
```

Example: Make a square layer by layer

```python
import libjackyprinto as ljp
from time import time,sleep
jp = ljp.jackyprinto()

start = time()
z_ret = 0
xytick = 2
jp.move(0,0,z_ret)
sleep(1)
jp.setPressure(2)
#get starting position
sign = 1
delay = .05
for z in range(20):
    for j in range(10):
        for i in range(10):
            jp.move(0,0,-z_ret)
            sleep(delay)
            sleep(delay)
            jp.togglePressure()
            sleep(delay)
            jp.move(0,0,z_ret)
            sleep(delay)
            jp.move(sign*xytick,0,0)
            sleep(delay)
        sleep(delay)
        sign = sign*-1
        jp.move(0,xytick,0)
    sleep(3)
    #jp.move(0,0,.04)
    jp.move(0,0,1,absolute=True)
    sign=1
    sleep(300)
    jp.move(0,0,0,absolute=True)
    sleep(3)
```
