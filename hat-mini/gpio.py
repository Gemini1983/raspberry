import time, configparser
#import RPi.GPIO library as GPIO
import RPi.GPIO as GPIO
#Set GPIO numbering scheme to pinnumber

config = configparser.ConfigParser()
config.read('config.ini')

def statePIN(numero_elettrovalvola):
    pin_eletrovalvola=int(config['pin'][numero_elettrovalvola])
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    #setup pin 18 as an output
    GPIO.setup(pin_eletrovalvola,GPIO.OUT)
    #lights off
    #GPIO.output(29,GPIO.LOW)
    stato=GPIO.input(pin_eletrovalvola)
    if stato==1:
        return "aperta"
    else:
        return "chiusa"

    #GPIO.output(29,GPIO.LOW)
    #lights on
    #GPIO.output(18,GPIO.LOW)