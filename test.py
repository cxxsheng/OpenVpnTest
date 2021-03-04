#!/usr/bin/python
# -*- coding: UTF-8 -*-
import getopt
import sys
import subprocess
import os
import platform

def test_ping(name, ip):
    print('test %s - %s' % (name,ip)),
    if platform.system() == "Darwin":
        ret = subprocess.call('ping -W 1000 -c 1 %s' % ip,stdout=subprocess.PIPE,shell=True)
    elif platform.system() == "Windows":
        ret = subprocess.call('ping -w 1000 -n 1 %s' % ip,stdout=subprocess.PIPE,shell=True)    
    else:
        ret = 1
    if ret == 0:
        print(' success')
    else:
        print(' failed')
    return ret           

def read_server_txt(filename):
    f = open(filename,"r")
    serverList = f.readlines()
    okList = ""
    serverCout = 0
    goodServerCout = 0
    for server in serverList:
        if server:
          name, ip   = server.split('-')
          name = name.strip()
          ip = ip.strip()
          serverCout += 1
          if(test_ping(name, ip) == 0):
            goodServerCout += 1  
            okList += server
    f.close()        
    return goodServerCout, serverCout, okList  


def read_server_dir(path):
    okList = ""
    serverCout = 0
    goodServerCout = 0
    unkownfileList = os.listdir(path)
    for unkownfilename in unkownfileList:
        if unkownfilename.endswith(".ovpn"):
            ovpnfile = open(os.path.join(path, unkownfilename))
            contentLines = ovpnfile.readlines()
            for oneline in contentLines:
                oneline = oneline.strip()
                if oneline.startswith('remote '):
                    ip = oneline.split()[1]
                    ip = ip.strip()
                    name = unkownfilename[:-5]
                    serverCout += 1
                    if(test_ping(name, ip) == 0):
                        goodServerCout += 1  
                        okList += ('%s - %s\n' % (name,ip))
            ovpnfile.close()
    return goodServerCout, serverCout, okList     


if len(sys.argv)<=1:
    print('usage: ./a.py filename or directory')
else:
    goodServerCout, serverCout = 0, 0
    okList = []
    filename = sys.argv[1]
    if filename.endswith(".txt"):
        goodServerCout, serverCout, okList = read_server_txt(filename)
    elif filename.endswith(".zip"):
        print("unsupported zip format parsing")
    else:
        if os.path.isdir(filename):
            goodServerCout, serverCout, okList = read_server_dir(filename)


    print("**************************************")           
    print("test finished, num: %d/%d, good server list is:" % (goodServerCout, serverCout))            
    print(okList)            
