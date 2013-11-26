CPUMonitorService
=================

A restful web service written in python in order to monitor CPU usage of multiple clients.

The project consists of a restful service written in python using flask
to generate a rest api to list the cpu usage of multiple devices been tracked.

It also has the code of the cpuAgent which when runned it registers to the service
and sends heartbeats with the cpu usage of the system. To send http requests, we
make use of the requests library

Also a simple rest client is included which uses jQuery javaScript, twitter bootstrap
framework and knockout in order to generate the views of the page and generate
the ajax HTTP requests to fetch the information from the service.


To run the system, first you need to configure the project first you need to 
generate a virtual environment for python to run. 

To do this on linux run for the monitor Service:

-python virtualenv.py flask
-flask/bin/pip install flask
-flask/bin/pip install flask-restful
-flask/bin/pip install flask-httpauth

To launch service:
-flask/bin/python MonitorService.py

For the agent do similar:

-python virtualenv.py flask
-flask/bin/pip install requests

To run the agent:
-flask/bin/python monitorAgent/cpuAgent.py [name-of-device]

Once the service is running, you can access the website on:
http://localhost:5000/index.html
