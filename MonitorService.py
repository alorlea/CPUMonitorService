#!flask/bin/python
'''
Created on Nov 23, 2013

@author: alberto lorente leal <albll@kth.se>, <a.lorenteleal@gmail.com>
'''
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.views import MethodView
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
api = Api(app)

devices=[
         {'id':1,
          'load': '50.0',
          'device': 'Samsung Galaxy S3'
          },
         {'id':2,
          'load': '30.0',
          'device': 'iPhone'
          },
         {'id':3,
          'load': '70.0',
          'device': 'NokiaLumia920'
          }
]

device_fields = {
                 'load':fields.String,
                 'device': fields.String,
                 'uri':fields.Url('device')
}

class DeviceListAPI(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('load', type = str, required = True, location = 'json')
        self.reqparse.add_argument('device', type = str, required = True, location = 'json')
        
        super(DeviceListAPI,self).__init__()
        
    def get(self):
        return { 'devices': map(lambda d: marshal(d,device_fields),devices)}
    
    def post(self):
        args = self.reqparse.parse_args()
        device = {
                  'id': devices[-1]['id'] + 1,
                  'load': args['load'],
                  'device': args['device']
        }
        devices.append(device)
        return {'device': marshal(device,device_fields)}, 201

class DeviceAPI(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('load', type = str, location='json')
        self.reqparse.add_argument('device', type = str, location='json')
        
        super(DeviceAPI,self).__init__()
        
    def get(self,id):
        device = filter(lambda d:d['id'] == id, devices)
        if len(device) ==0:
            abort(404)
        return {'device': marshal(device[0],device_fields)}
    
    def put(self,id):
        device = filter(lambda d:d['id'] == id,devices)
        if len(device)==0:
            abort(404)
        device = device[0]
        args = self.reqparse.parse_args()
        device['load'] = args.get('load', device['load'])
        device['device'] = args.get('device',device['device'])
        
        return {'device': marshal(device, device_fields)}
    
    def delete(self,id):
        device = filter(lambda d:d['id']==id,devices)
        if len(device)== 0:
            abort(404)
        devices.remove(device[0])
        return {'return':True}

api.add_resource(DeviceListAPI, '/CPUMonitor/api/v0.1/devices', endpoint='devices')
api.add_resource(DeviceAPI, '/CPUMonitor/api/v0.1/devices/<int:id>', endpoint ='device')

if __name__ =='__main__':
    app.run(debug = True,host='0.0.0.0')
