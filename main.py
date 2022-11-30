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


# Define Motors Here
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

    gpio.setup(17, gpio.OUT)
    gpio.setup(18, gpio.OUT)

    gpio.setup(27, gpio.OUT)
    gpio.setup(22, gpio.OUT)

    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

    gpio.setup(5, gpio.OUT)
    gpio.setup(6, gpio.OUT)
except:
    print("GPIO SETUP FAILED!, EXITING TO PREVENT FUTURE PROBLEMS")
    exit()

print("GPIO SETUP COMPLETE")

print("Setting up HTTP WEB SERVICE")

@api.route('/ping', methods=['GET'])
def ping():
    return 'Pong'

@api.route('/forward', methods=['GET'])
def forward():
    motor.forward(M1)
    motor.forward(M2)
    motor.forward(M3)
    motor.forward(M4)
    return 'Command Received'

@api.route('/reverse', methods=['GET'])
def reverse():
    motor.reverse(M1)
    motor.reverse(M2)
    motor.reverse(M3)
    motor.reverse(M4)
    return 'Command Received'

@api.route('/stop', methods=['GET'])
def stop():
    motor.stop(M1)
    motor.stop(M2)
    motor.stop(M3)
    motor.stop(M4)
    return 'Command Received'

@api.route('/move_left', methods=['GET'])
def move_left():
    motor.forward(M1)
    motor.reverse(M2)
    motor.reverse(M3)
    motor.forward(M4)
    return 'Command Received'

@api.route('/move_right', methods=['GET'])
def move_right():
    motor.reverse(M1)
    motor.forward(M2)
    motor.forward(M3)
    motor.reverse(M4)
    return 'Command Received'


if __name__ == '__main__':
    api.run(host='0.0.0.0')

print('Finish setting up API Server')
