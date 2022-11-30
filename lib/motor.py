import RPi.GPIO as GPIO

def forward(pin):
    GPIO.output(pin, GPIO.HIGH)

def reverse(pin):
    GPIO.output(pin, GPIO.HIGH)

GPIO.cleanup()