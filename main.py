import RPi.GPIO as gpio
from flask import Flask, json
import time
import lib.motor as motor

api = Flask(__name__)
gpio.cleanup()

print("""
CS Day Wheeler V1
Coded By Yanavut Rojanapron
https://github.com/chokunplayz
""")

print("setting up GPIO MODE")

gpio.setwarnings(False)

try :
    gpio.setmode(gpio.BCM)

    gpio.setup(16, gpio.OUT)
    gpio.setup(18, gpio.OUT)
except:
    print("GPIO SETUP FAILED!, EXITING TO PREVENT FUTURE PROBLEMS")
    exit()

print("GPIO SETUP COMPLETE")

print("Setting up HTTP WEB SERVICE")

@api.route('/ping', methods=['GET'])
def ping():
    return 'Pong'

if __name__ == '__main__':
    api.run()

