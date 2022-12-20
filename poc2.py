import cv2
import numpy as np
import RPi.GPIO as gpio
from flask import Flask, jsonify, Response
import time
import lib.motor as motor
import lib.mecanum as mecanum
import subprocess
import threading
import picamera
import io

app = Flask(__name__, static_folder='page')

cap = None

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

def create_response(success, code, message):
    if success:
        return jsonify({'success': success, 'code': code, 'message': message})
    else:
        return jsonify({'success': success, 'error_code': code, 'error_message': message})

@app.route('/api/v1/ping', methods=['POST','GET'])
def ping():
    return create_response(True, 200, 'Pong')

@app.route('/api/v1/forward', methods=['POST'])
def forward_api():
    mecanum.forward(M1, M2, M3, M4)
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/reverse', methods=['POST'])
def reverse_api():
    mecanum.reverse(M1, M2, M3, M4)
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/stop', methods=['POST'])
def stop_api():
    mecanum.stop(M1, M2, M3, M4)
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/move_left', methods=['POST'])
def move_left_api():
    mecanum.move_left(M1, M2, M3, M4)
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/move_right', methods=['POST'])
def move_right_api():
    mecanum.move_right(M1, M2, M3, M4)
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/turn_left', methods=['POST'])
def turn_left_api():
    mecanum.turn_left(M1, M2, M3, M4)
    return create_response(True, 200, 'Command Received')

@app.route('/api/v1/turn_right', methods=['POST'])
def turn_right_api():
    mecanum.turn_right(M1, M2, M3, M4)
    return create_response(True, 200, 'Command Received')

# Global variable to enable/disable auto steer
auto_steer_enabled = False

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace;')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 24

    def get_frame(self):
        frame = io.BytesIO()
        self.camera.capture(frame, 'jpeg', use_video_port=True)
        frame.seek(0)
        return frame.read()

# API endpoint to enable/disable auto steer
@app.route('/api/v1/auto_steer', methods=['POST'])
def auto_steer_api():
    global auto_steer_enabled

    # Toggle the value of the global variable
    auto_steer_enabled = not auto_steer_enabled

    if auto_steer_enabled:
        return create_response(True, 200, 'Auto steer enabled')
    else:
        return create_response(True, 200, 'Auto steer disabled')

@app.route('/api/v1/auto_steer/status', methods=['GET'])
def get_auto_steer_status():
    global auto_steer_enabled
    return jsonify({'auto_steer_enabled': auto_steer_enabled})

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/v1/shutdown', methods=['POST'])
def shutdown():
    shutdown_command = "sudo shutdown -h now"
    process = subprocess.Popen(shutdown_command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return create_response(True, 200, output)

# Main function
def main():
    # Set up the GPIO pins
    setup_gpio()

    # Start the Flask API
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
