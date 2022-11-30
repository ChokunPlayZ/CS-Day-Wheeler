import RPi.GPIO as GPIO

def forward(motor):
    GPIO.output(motor['forward'], GPIO.HIGH)

def reverse(motor):
    GPIO.output(motor['reverse'], GPIO.HIGH)