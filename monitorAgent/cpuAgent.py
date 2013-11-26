#!usr/bin/env python
'''
Created on Nov 23, 2013

A python agent that monitors CPU usage
On a first run, it registers to the rest service with a POST request
and periodically sends a heartbeat back on the status of the CPU usage.

It has simple authentication against the rest service.
It is disabled but can be reenabled by uncommenting the respective
security credentials an authentication.

@author: alberto lorente leal <albll@kth.se>,<a.lorenteleal@gmail.com>
'''
from sys import argv
import os
import time
import requests
import json
import multiprocessing

script, device = argv
endpoint='http://localhost:5000'
server_url=endpoint + '/CPUMonitor/api/v0.1/devices'
period = 5
#user = 'admin'
#password = 'admin'
device_uri= ''
cores = multiprocessing.cpu_count()
class Register:
    def __init__(self):
        while True:
            register = Register.registerDevice()
            if register:
                break
            time.sleep(period)
            
    @staticmethod
    def registerDevice():

        load = os.getloadavg()
        payload={'cpu':(load[0]/cores)*100,'load':load,'name':device}
        headers = {'content-type': 'application/json'}
        #auth = (user, password)
        #response = requests.post(server_url,data=json.dumps(payload),auth=auth,headers=headers)
        response = requests.post(server_url,data=json.dumps(payload),headers=headers)
        print response.json()
        if response.status_code == 201:
            json_data = response.json()
            global device_uri 
            device_uri = endpoint + json_data['device']['uri']
            print device_uri
            return True
        return False
    
class CPUHeartbeat:
    def __init__(self):
        while True:
            CPUHeartbeat.sendCPU()
            time.sleep(period)
            
        
    @staticmethod
    def sendCPU():
        load = os.getloadavg()
        
        payload={'cpu':(load[0]/cores)*100,'load':load,'name':device}
        headers = {'content-type': 'application/json'}
        #auth = (user, password)
        print device_uri
        #response = requests.put(device_uri,data=json.dumps(payload),auth=auth,headers=headers)
        response = requests.put(device_uri,data=json.dumps(payload),headers=headers)
        if response.status_code == 200:
            print 'updated the value in the database'
        
Register()
CPUHeartbeat()