#This file tests a lot of things on the motors

import time
from DistanceCalculator import DistanceCalculator
from CSVParser import CSVParser
from Navigator import Navigator
from MotorControl import MotorControl
from MotorSimulator import MotorSimulator
from DistanceCalculator import DistanceCalculator
from OpenCVSimulator import OpenCVSimulator
from CSVParser import CSVParser
from Field import Field
motorcontrol = 0

def main():
    data_amount = 10
    error_level = 0.0
    parser = CSVParser()
    field_location = "field.csv"
    parsed_format = parser.parse(field_location)
    field = Field(parsed_format)
    left_motor = MotorSimulator()
    right_motor = MotorSimulator()
    vert_motor = MotorSimulator()
    error_levelIP = 1
    velocity_error = 0.01
    angular_instability = 0.01
    image_processor = OpenCVSimulator(error_levelIP, velocity_error, angular_instability)
    motor_control = MotorControl(left_motor, right_motor, vert_motor)
    distance_calculator = DistanceCalculator(error_level, data_amount)
    navigator = Navigator(field, distance_calculator, motor_control, image_processor)
    distance_calculator.navigator = navigator
    image_processor.navigator = navigator
    
    navigator.start()
    distance_calculator.start()
    
    

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
    
def up_test():
    #Remember, only testing motors, nothing more (like the stabilize function)
    for level in range(0, 10, 1):
        motorcontrol.vert.level(1)
        print "Spinning vertical motor up for 3 seconds"
        time.sleep(3)
        motorcontrol.vert_off()
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