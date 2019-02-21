#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

#  _    _            _ _   _        _____ _               _    
# | |  | |          | | | | |      / ____| |             | |   
# | |__| | ___  __ _| | |_| |__   | |    | |__   ___  ___| | __
# |  __  |/ _ \/ _` | | __| '_ \  | |    | '_ \ / _ \/ __| |/ /
# | |  | |  __/ (_| | | |_| | | | | |____| | | |  __/ (__|   < 
# |_|  |_|\___|\__,_|_|\__|_| |_|  \_____|_| |_|\___|\___|_|\_\
#
#                                                               

#
# Author:  Lapshin Sergey [ sergey@lapshin.pro ]
#

import os, sys, subprocess, json, yaml
from flask import Flask
from flask import Response
from flask import request

def conf_load():
  with open('hc.yaml','r') as f:
    conf = yaml.load(f)
  return conf

def init_status():
  status={'status':'ok'}
  return json.dumps(status)

def get_auth_services():
  return json.dumps(authorized_services)

def get_service(service):
  if service not in authorized_services:
    return json.dumps({'status':'error','error':'not authorized service'})
  key_value = subprocess.check_output(['systemctl', 'show', service], universal_newlines=True).split('\n')	
  json_dict = {}
  for entry in key_value:
    kv = entry.split("=", 1)
    if len(kv) == 2:
      json_dict[kv[0]] = kv[1]
  return json.dumps(json_dict)

# Conf load
conf = conf_load()
authorized_services = conf['server']['services']

# Flask
app = Flask(__name__)
@app.route("/")
def start():
  return Response(init_status(), mimetype='application/json')

@app.route("/services")
def services():
  return Response (get_auth_services(), mimetype='application/json')

@app.route("/service/<service>")
def service (service):
  return Response (get_service(service), mimetype='application/json')

if __name__ == "__main__":
    app.run('0.0.0.0', port=9755)
