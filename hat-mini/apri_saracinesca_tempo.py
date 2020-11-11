#!/usr/bin/env python3

import sys, os, automationhat, configparser, datetime, time, signal

config = configparser.ConfigParser()
config.read('config.ini')

path_project=os.path.abspath(os.path.dirname(sys.argv[0]))

id_valvola=sys.argv[1]
automationhat.output[int(id_valvola)-1].write(1)

if len(sys.argv) > 2:
    tempo_apertura=int(sys.argv[2])    
else:
    tempo_apertura=int(config['definition']['default_apertura_manuale'])
    
time.sleep(tempo_apertura)
automationhat.output[int(id_valvola)-1].write(0)






