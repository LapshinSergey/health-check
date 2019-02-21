#!/usr/bin/python3.4
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

import os, sys, subprocess, json, locale, requests, yaml
#from flask import request
from dialog import Dialog

class RequestIterator(object):
  def __init__(self):
    #self.response = requests.get('http://localhost:9755/service/'+link)
    #self.services = sevices
    pass
  def __iter__(self):
    return self
  def next(self):
    response = requests.get('http://localhost:9755/service/'+self.services)
    return response
    

dg = Dialog(dialog='dialog', autowidgetsize=True)
dg.set_background_title('Health Check\tdsadsada')


def conf_load():
  with open('hc.yaml','r') as f:
    conf = yaml.load(f)
  return conf


servers=[('localhost','Check')]


def server_menu():
  menu = dg.menu('Index', choices=servers)
  return menu

def health_services_menu(responses):
  servers = [(item['Id'],item['LoadState']) for item in responses]
  print (servers)
  return dg.menu('Health Services:',choices=servers)

def msgbox(text):
  menu = dg.msgbox(text)

def errorbox(text, width=100):
  menu = dg.msgbox(text)

while 1: 
  choices = server_menu()
  if choices[0] == 'ok':
    try:
      response = requests.get('http://'+choices[1]+':9755/services')
    except requests.exceptions.ConnectionError:
      errorbox('Failed to establish a new connection: \n[Errno 111] Connection refused')
      continue
    services = json.loads(response.text)
    responses = [json.loads(requests.get('http://'+choices[1]+':9755/service/'+item).text) for item in services] 
    health_services_menu_choice = health_services_menu(responses)
    if health_services_menu_choice[0] == 'cancel':
      continue
    else:
      print (health_services_menu_choice[1])
  else:
    break

clear = lambda: os.system('clear')
clear()
print ('GoodBuy') 
