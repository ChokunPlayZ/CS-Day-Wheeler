import cv2
import numpy as np
import RPi.GPIO as gpio
from flask import Flask, jsonify, Response
import time
import lib.motor as motor
import lib.mecanum as mecanum
import subprocess
import threading

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

def detect_lines():
    # Capture video from camera or video file
    global cap
    cap = cv2.VideoCapture(0)

    # Set up the mjpeg stream
    ret, frame = cap.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    frame = frame.tobytes()

@app.route('/video_feed')
def video_feed():
    return Response(gen(cap),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(cap):
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply a blur to the image
        blur = cv2.GaussianBlur(gray, (5,5), 0)

        # Detect edges in the image using the Canny function
        edges = cv2.Canny(blur, 50, 150)

        # Detect lines in the image using the HoughLinesP function
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=10, maxLineGap=250)

        # Draw the detected lines on the original image
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Determine the center of the image
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2

        # Draw a circle at the center of the image
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        # If auto steer is enabled, adjust the robot's movement based on the position of the detected lines
        if auto_steer_enabled:
            # Initialize variables to store the average position of the lines
            avg_x1 = 0
            avg_x2 = 0
            num_lines = 0

            # Iterate through the detected lines and calculate the average position
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    avg_x1 += x1
                    avg_x2 += x2
                    num_lines += 1

                # If there are no lines detected, stop the robot
                if num_lines == 0:
                    mecanum.stop(M1, M2, M3, M4)
                else:
                    avg_x1 = avg_x1 // num_lines
                    avg_x2 = avg_x2 // num_lines

                    # Calculate the average position of the lines
                    avg_pos = (avg_x1 + avg_x2) // 2

                    # If the average position is to the left of the center, move the robot to the right
                    if avg_pos < center_x:
                        mecanum.move_right(M1, M2, M3, M4)
                    # If the average position is to the right of the center, move the robot to the left
                    elif avg_pos > center_x:
                        mecanum.move_left(M1, M2, M3, M4)
                    # If the average position is close to the center, keep the robot moving forward
                    else:
                        mecanum.forward(M1, M2, M3, M4)

            # Encode the frame as a JPEG image
            result, frame = cv2.imencode('.jpg', frame, encode_param)

            # Convert the frame to a bytes object
            frame = frame.tobytes()

            # Yield the frame to the mjpeg stream
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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

    # Start the line detection loop in a separate thread
    line_detection_thread = threading.Thread(target=detect_lines)
    line_detection_thread.start()

    # Start the Flask API
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
