import RPi.GPIO as GPIO

def forward(motor):
    GPIO.output(motor['forward'], GPIO.HIGH)
    GPIO.output(motor['reverse'], GPIO.LOW)

def reverse(motor):
    GPIO.output(motor['forward'], GPIO.LOW)
    GPIO.output(motor['reverse'], GPIO.HIGH)