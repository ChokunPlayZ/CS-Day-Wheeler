def forward(motor, ):
    GPIO.output(motor['forward'], GPIO.HIGH)
    GPIO.output(motor['reverse'], GPIO.LOW)