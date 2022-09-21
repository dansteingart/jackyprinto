##Author: Dan Steingart
##Date Started: 2022-01-10
##Notes: Jacky Printo Library

import requests
import json
from time import sleep, time
from subprocess import getoutput as go
import sys

class jackyprinto:
    def __init__(self,
        project="test",
        prefix="snap",
        user="user",
        url = "http://localhost",
        ender_port = "3000",
        ultimus_port="9001",
        notes = None,
        practice = False):
        '''Instantiate jackyprinto instance'''
        self.url  = url + ":" + ender_port
        self.durl = url + ":" + ultimus_port
        self.project = project
        self.prefix = prefix
        self.user = user
        self.notes = notes
        self.camera = self.get_v4l2_ctls(values_only=True) 
        self.practice = practice
    
    def _ready(self,cmd,data):
        '''Package the Ultimus command for download to device'''
        cmd = str(cmd)
        data = str(data)
        size = str(len(cmd+data)).zfill(2)
        out = '\x02' \
            + size \
            + cmd \
            + data \
            + self._EFD_checksum(size+cmd+data) \
            + '\x03'
        return out

    def _EFD_checksum(self,s):
        '''EFD checksum calculator'''
        check = hex( (0-sum(ord(x) for x in s))&255 )
        return check[2:].upper()

    def send_to_stage(self,cmd):
        '''Send Marlin GCode Commands to Ender Stages'''
        cmd = {'payload':cmd}
        foo = requests.post(f"{self.url}/write",data=cmd)
        return foo.text

    def get_snapshot_old(self,base="files",pat="snap",meta=""):
        '''[DEPRECATED] Take a snapshot'''
        fn = f"{base}/{pat}_{meta}_{int(time())}.jpg"
        go(f"curl {curl}/snapshot --output {fn}")

    def get_snapshot(self):
        '''Take a snapshot'''
        out = {}
        out['project'] = self.project
        out['prefix']  = self.prefix
        out['user']    = self.user
        out['notes']   = self.notes
        out['position'] = self.get_position()
        out['camera']  = self.camera
        out['date']    = int(time()*1000)
        ret = requests.post(f"{self.url}/snapshot",json=out).json()
        return ret
        #data['project'] =$("#project").val()

    def steppers_off(self):
        '''Turn off stepper motors'''
        return send_to_stage(f"M18 X Y Z")

    def move(self,x,y,z,absolute=False):
        '''Move relative to x/y/z, unless absolute flag is ticked
        If None is specified don't change that position'''
        if absolute: pre = "G90"
        else:        pre = "G91"
        X = Y = Z = ""
        if x != None: X = f'X{x}'
        if y != None: Y = f'Y{y}'
        if z != None: Z = f'Z{z}'
        return self.send_to_stage(f"{pre}\nG0 {X} {Y} {Z}")

    def get_v4l2_ctls(self,values_only = False):
        '''Get V4L2 states'''
        foo = requests.post(f"{self.url}/v4l2-ctl-list").json()['ctls']
        if values_only:
            goo = {}
            for f in foo.keys(): goo[f] = foo[f]['value']
            foo = goo
        return foo    
        
        return foo

    def get_position(self):
        '''Get Position'''
        out = {} 
        foo = requests.get(f"{self.url}/get_current_position").json()['current_position']
        for f in foo.keys():
            out[f.lower()] = foo[f]

        return out

    #---commands---
    def togglePressure(self): 
        '''Fire dispenser'''
        out = self._ready("DI  ","")
        self.send_to_dispenser(out)
        return out

    def setPressure(self,pressure):
        '''Set Pressure (PSI)'''
        s = f'{pressure:.1f}'.replace(".","").rjust(4,"0")
        out = f"PS  {s}"

        self.send_to_dispenser(out)
        return out

    def setDispenseTime(self,dispensetime):
        '''Set Dispense Time (s)'''
        s = f'{dispensetime:.4f}'.replace(".","").rjust(5,"0")
        out = f"DS  {s}"
        self.send_to_dispenser(out)
        return out

    def setVacuum(self,dispensetime):
        '''Set Vacuum (Torr)'''
        s = f'{pressure:.1f}'.replace(".","").rjust(4,"0")
        out = f"VS  {s}"
        self.send_to_dispenser(out)
        return out

    def send_to_dispenser(self,cmd):
        '''Send download commands to printer'''
        if not self.practice: requests.post(self.durl+"/write",data={'payload':'\x05'+cmd})
        elif self.practice: print(cmd)





if "__main__" == __name__:
    jp = jackyprinto(project="test_python_lib",prefix="snap",user="dan",practice=False
    )
    start = time()
    z_ret = 0

    jp.move(0,0,z_ret)
    sleep(1)
    #jp.setPressure(2)
    # #get starting position
    # sign = 1
    # delay = .05
    # for j in range(10):
    #     for i in range(10):
    #         p1 = jp.get_position()
    #         jp.move(0,0,-z_ret)
    #         sleep(delay)
    #         #jp.send_to_stage("M400\r\n")
    #         sleep(delay)
    #         #jp.send_to_stage("M118 _DA:04DI  CF\r\n")
    #         jp.togglePressure()
    #         sleep(delay)
    #         jp.move(0,0,z_ret)
    #         sleep(delay)
    #         jp.move(sign*.5,0,0)
    #         sleep(delay)
    #     sleep(delay)
    #     sign = sign*-1
    #     jp.move(0,.5,0)
    # jp.move(0,0,-z_ret)##Author: Dan Steingart
