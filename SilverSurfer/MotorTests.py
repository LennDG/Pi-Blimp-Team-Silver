#This file tests a lot of things on the motors

import ZeppelinControl, Motor, time

def main():
    frequency = 10

    # Left motor
    cw_pin = 24
    ccw_pin = 4
    left_motor = Motor.Motor(cw_pin, ccw_pin, frequency)
    left_motor.start()

    # Right motor
    cw_pin = 17
    ccw_pin = 23
    right_motor = Motor.Motor(cw_pin, ccw_pin, frequency)

    # Vertical motor
    cw_pin = 7
    ccw_pin = 9
    vert_motor = Motor.VerticalMotor(cw_pin, ccw_pin)
    zep_control = ZeppelinControl.ZeppelinControl(0)
    up_test(zep_control)
    up_test(zep_control)
    up_test(zep_control)
    
    

def forward_test(zep_control, parameter):
    print "Testing forward movement for 3 seconds"
    zep_control.move(1)
    time.sleep(parameter)
    print "stopping forward movement"
    zep_control.hor_stop()
    time.sleep(30)
    
def backward_test(zep_control):
    print "Testing backward movement for 3 seconds"
    zep_control.move(-1)
    time.sleep(3)
    print "stopping backward movement"
    zep_control.hor_stop()
    time.sleep(1)
    
def left_turn_test(zep_control):
    print "Testing left turn for 3 seconds"
    zep_control.turn(1)
    time.sleep(3)
    print "Stopping turn"
    zep_control.hor_stop()
    time.sleep(1)
    
def right_turn_test(zep_control):
    print "Testing right turn for 3 seconds"
    zep_control.turn(-1)
    time.sleep(3)
    print "Stopping turn"
    zep_control.hor_stop()
    time.sleep(1)
    
def up_test(zep_control):
    #Remember, only testing motors, nothing more (like the stabilize function)
    for level in range(0, 10, 1):
        zep_control.vert_move(100)
        print "Spinning vertical motor up for 3 seconds"
        time.sleep(3)
        zep_control.shutoff
        print "Stopping vertical movement"
        time.sleep(3)

def down_test(zep_control):
    #Remember, only testing motors, nothing more (like the stabilize function)
    print "Spinning vertical motor down for 3 seconds"
    for level in range(0, -100, -10):
        zep_control.vert_move(level)
        time.sleep(0.5)
    print "Stopping vertical movement"
    zep_control.shutoff()
    time.sleep(1)

def stabilize_test(zep_control):
    #TODO: implement this, maybe stabilize needs to say the zeppelin is stable?
    pass

main()