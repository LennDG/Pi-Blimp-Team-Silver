#This file tests a lot of things on the motors

import ZeppelinControl, Motor, time

def main():
    zep_control = ZeppelinControl.ZeppelinControl()
    

def forward_test(zep_control):
    print "Testing forward movement for 3 seconds"
    zep_control.move(1)
    time.sleep(3)
    print "stopping forward movement"
    zep_control.hor_stop()
    
def backward_test(zep_control):
    print "Testing backward movement for 3 seconds"
    zep_control.move(-1)
    time.sleep(3)
    print "stopping backward movement"
    zep_control.hor_stop()
    
def left_turn_test(zep_control):
    print "Testing left turn for 3 seconds"
    zep_control.turn(1)
    time.sleep(3)
    print "Stopping turn"
    zep_control.hor_stop()
    
def right_turn_test(zep_control):
    print "Testing right turn for 3 seconds"
    zep_control.turn(-1)
    time.sleep(3)
    print "Stopping turn"
    zep_control.hor_stop()
    
def up_test(zep_control):
    #TODO: not sure how to implement this
    pass

def down_test(zep_control):
    #TODO: not sure how to implement this
    pass

def stabilize_test(zep_control):
    #TODO: implement this, maybe stabilize needs to say the zeppelin is stable?
    pass

