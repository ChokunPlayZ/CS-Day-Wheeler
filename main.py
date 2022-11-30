import RPi.GPIO as gpio
from flask import Flask, json
import time
import lib.motor as motor
# import lib.mecanum as wheeler

api = Flask(__name__)
gpio.cleanup()

print("""
CS Day Wheeler V1
Coded By Yanavut Rojanapron
https://github.com/chokunplayz
""")

print("setting up GPIO MODE")

gpio.setwarnings(False)


# Defone Motors Here
M1 = {
    "forward": 17,
    "reverse": 18
}

M2 = {
    "forward": 27,
    "reverse": 22
}

M3 = {
    "forward": 23,
    "reverse": 24
}

M4 = {
    "forward": 5,
    "reverse": 6
}

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
