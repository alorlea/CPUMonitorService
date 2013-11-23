#!usr/bin/env python
'''
Created on Nov 23, 2013

@author: alberto lorente leal <albll@kth.se>,<a.lorenteleal@gmail.com>
'''

import os
import time
import requests
import json

endpoint='http://localhost:5000'
server_url=endpoint + '/CPUMonitor/api/v0.1/devices'
period = 5
user = 'FilesFromYou'
password = 'YouFromFiles'
device_uri= ''
load = 0

class Register:
    def __init__(self):
        while True:
            register = Register.registerDevice()
            if register:
                break
            time.sleep(period)
            
    @staticmethod
    def registerDevice():
        payload={'load':'50','device':'test'}
        headers = {'content-type': 'application/json'}
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
        global load
        load= load +period
        payload={'load':load,'device':'test'}
        headers = {'content-type': 'application/json'}
        print device_uri
        response = requests.put(device_uri,data=json.dumps(payload),headers=headers)
        if response.status_code == 200:
            print 'updated the value in the database'
        
    

Register()
CPUHeartbeat()