"""
This file initialises our version of the zeppelin and starts running the program.

@author Rob Coekaerts
@version 0.0   7-3-2014
"""

from Zeppelin import Zeppelin
from ImageRecognitionClient import ImageRecognitionClient
from Navigator import Navigator
from MotorControl import MotorControl
import Motor
from DistanceSensor import DistanceSensor
import CSVParser
from Field import Field


""" Motors """
frequency = 10

# Left motor
cw_pin = 11
ccw_pin = 10
left_motor = Motor.Motor(cw_pin, ccw_pin, frequency)
left_motor.start()

# Right motor
cw_pin = 23
ccw_pin = 17
right_motor = Motor.Motor(cw_pin, ccw_pin, frequency)
right_motor.start()

# Vertical motor
cw_pin = 7
ccw_pin = 9
vert_motor = Motor.VerticalMotor(cw_pin, ccw_pin)


""" Motor control"""

motor_control = MotorControl(left_motor, right_motor, vert_motor)


""" Distance sensor """

# Determines of how many values the median is taken in the distance sensor
data_amount = 10

distance_sensor = DistanceSensor(data_amount)


""" Field """

# Create a parser to parse the field
parser = CSVParser.CSVParser()

# Name of the file containing the field
field_location = "field.csv"

# Parsed format of field
parsed_format = parser.parse(field_location)

# Construction of the field object.
field = Field(parsed_format)


""" Image processing """

# OpenCV 
image_processor = ImageRecognitionClient()


""" Navigator """

navigator = Navigator(field, distance_sensor, motor_control, image_processor)
navigator.start()
image_processor.navigator = navigator

""" Zeppelin """

name='zilver'
zeppelin = Zeppelin(navigator,name)
zeppelin.start()

