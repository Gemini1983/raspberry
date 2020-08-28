import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

for x in range(int(config['definition']['numero'])):
    print(config['valves'][str(x+1)])
    

try:
    print(config['valves'][str(1)])
except:
    print("Errore, ")
