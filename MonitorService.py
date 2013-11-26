#!flask/bin/python
'''
Created on Nov 23, 2013

Restful service based on the flask python library using
its restful tools.

Contains a restful api to list all the devices registered on the service
with their metrics. It supports GET and POST operations

For each device we have also its personal restful api to query on a specific
device. It supports GET, PUT and DELETE operations.

Has support for authentication against the rest service. Disabled
the auth security, to reenable uncomment those parts of the code

@author: alberto lorente leal <albll@kth.se>, <a.lorenteleal@gmail.com>
'''
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.views import MethodView
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
api = Api(app)

#auth = HTTPBasicAuth()
 
#@auth.get_password
#def get_password(username):
#    if username == 'admin':
#        return 'admin'
#    return None
#
#@auth.error_handler
#def unauthorized():
#    return make_response(jsonify( { 'message': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    

devices=[
         {'id':1,
          'cpu': '50.0',
          'load':'[0.3,0.6,0.7]',
          'name': 'Samsung Galaxy S3'
          },
         {'id':2,
          'cpu': '30.0',
          'load': '[0.3,0.6,0.7]',
          'name': 'iPhone'
          },
         {'id':3,
          'cpu': '70.0',
          'load': '[0.3,0.6,0.7]',
          'name': 'NokiaLumia920'
          }
]

device_fields = {
                 'load':fields.String,
                 'cpu': fields.String,
                 'name': fields.String,
                 'uri':fields.Url('device')
}

class DeviceListAPI(Resource):
    #decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('load', type = str, required = True, location = 'json')
        self.reqparse.add_argument('name', type = str, required = True, location = 'json')
        self.reqparse.add_argument('cpu',type=str,required = True, location = 'json')
        
        super(DeviceListAPI,self).__init__()
        
    def get(self):
        return { 'devices': map(lambda d: marshal(d,device_fields),devices)}
    
    def post(self):
        args = self.reqparse.parse_args()
        device = {
                  'id': devices[-1]['id'] + 1,
                  'load': args['load'],
                  'name': args['name'],
                  'cpu': args['cpu']
        }
        devices.append(device)
        return {'device': marshal(device,device_fields)}, 201

class DeviceAPI(Resource):
    #decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('load', type = str, location='json')
        self.reqparse.add_argument('name', type = str, location='json')
        self.reqparse.add_argument('cpu',type=str, location = 'json')
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
        device['name'] = args.get('name',device['name'])
        device['cpu'] = args.get('cpu',device['cpu'])
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
