import lib.motor as motor
def forward(M1, M2, M3, M4):
    motor.forward(M1)
    motor.forward(M2)
    motor.forward(M3)
    motor.forward(M4)

def reverse(M1, M2, M3, M4):
    motor.reverse(M1)
    motor.reverse(M2)
    motor.reverse(M3)
    motor.reverse(M4)

def stop(M1, M2, M3, M4):
    motor.stop(M1)
    motor.stop(M2)
    motor.stop(M3)
    motor.stop(M4)

def move_left(M1, M2, M3, M4):
    motor.forward(M1)
    motor.reverse(M2)
    motor.reverse(M3)
    motor.forward(M4)
   
def move_right(M1, M2, M3, M4):
    motor.reverse(M1)
    motor.forward(M2)
    motor.forward(M3)
    motor.reverse(M4)

def turn_left(M1, M2, M3, M4):
    motor.forward(M1)
    motor.reverse(M2)
    motor.forward(M3)
    motor.reverse(M4)

def turn_right(M1, M2, M3, M4):
    motor.reverse(M1)
    motor.forward(M2)
    motor.reverse(M3)
    motor.forward(M4)