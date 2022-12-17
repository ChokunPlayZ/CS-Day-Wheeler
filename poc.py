import RPi.GPIO as gpio
from flask import Flask, jsonify
import time
import lib.motor as motor
import subprocess

app = Flask(__name__, static_folder='page')

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

def motor_setup(motor_name):
    if "forward" in motor_name and "reverse" in motor_name:
        forward_pin = motor_name["forward"]
        reverse_pin = motor_name["reverse"]
        gpio.setup(forward_pin, gpio.OUT)
        gpio.setup(reverse_pin, gpio.OUT)
    else:
        raise ValueError("Error: Forward and reverse pins must be defined for the motor.")

def setup_gpio():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)

    motor_setup(M1)
    motor_setup(M2)
    motor_setup(M3)
    motor_setup(M4)

def forward():
    motor.forward(M1)
    motor.forward(M2)
    motor.forward(M3)
    motor.forward(M4)

def reverse():
    motor.reverse(M1)
    motor.reverse(M2)
    motor.reverse(M3)
    motor.reverse(M4)

def stop():
    motor.stop(M1)
    motor.stop(M2)
    motor.stop(M3)
    motor.stop(M4)

def move_left():
    motor.forward(M1)
    motor.reverse(M2)
    motor.reverse(M3)
    motor.forward(M4)
   
def move_right():
    motor.reverse(M1)
    motor.forward(M2)
    motor.forward(M3)
    motor.reverse(M4)

def turn_left():
    motor.forward(M1)
    motor.reverse(M2)
    motor.forward(M3)
    motor.reverse(M4)

def turn_right():
    motor.reverse(M1)
    motor.forward(M2)
    motor.reverse(M3)
    motor.forward(M4)

def create_response(success, code, message):
    if success:
        return jsonify({'success': success, 'code': code, 'message': message})
    else:
        return jsonify({'success': success, 'error_code': code, 'error_message': message})

@app.route('/api/v1/ping', methods=['POST'])
def ping():
    return create_response(True, 200, 'Pong')

@app.route('/api/v1/forward', methods=['POST'])
def forward_api():
    forward()
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/reverse', methods=['POST'])
def reverse_api():
    reverse()
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/stop', methods=['POST'])
def stop_api():
    stop()
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/move_left', methods=['POST'])
def move_left_api():
    move_left()
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/move_right', methods=['POST'])
def move_right_api():
    move_right()
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/turn_left', methods=['POST'])
def turn_left_api():
    turn_left()
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/turn_right', methods=['POST'])
def turn_right_api():
    turn_right()
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/shutdown', methods=['POST'])
def shutdown():
    shutdown_command = "sudo shutdown -h now"
    process = subprocess.Popen(shutdown_command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return create_response(True, 200, output)


@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    setup_gpio()
    app.run(host='0.0.0.0')

