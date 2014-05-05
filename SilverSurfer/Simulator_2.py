"""
This file initialises our version of the zeppelin and starts running the program.

@author Rob Coekaerts
@version 0.9   7-3-2014
"""
from Zeppelin import Zeppelin
#from TestZeppelin import Zeppelin
from Navigator import Navigator
from MotorControl import MotorControl
from MotorSimulator import MotorSimulator
from DistanceCalculator import DistanceCalculator
from OpenCVSimulator import OpenCVSimulator
from CSVParser import CSVParser
from SimulatorField import Field


""" Motors """

# Left motor
left_motor = MotorSimulator()
# Right motor
right_motor = MotorSimulator()
# Vertical motor
vert_motor = MotorSimulator()


""" Motor control"""

motor_control = MotorControl(left_motor, right_motor, vert_motor)


""" Distance sensor """

# Determines of how many values the median is taken in the distance sensor
data_amount = 10
# Determines the mean error on the readings
error_level = 0.0

distance_calculator = DistanceCalculator(error_level, data_amount)


""" Field """

# Create a parser to parse the field
parser = CSVParser()

# Name of the file containing the field
field_location = "field.csv"

# Parsed format of field
parsed_format = parser.parse(field_location)

# Construction of the field object.
field = Field(parsed_format)


""" Image processing """

# OpenCV, For now, the simulated version is used as the real one is not available yet.

# The mean deviation from the images of nodes are from their supposed position in pixels.
error_level = 1
# The mean deviation in the angle of the velocity vector from its supposed value
velocity_error = 0.01
angular_instability = 0.0000000000000001

image_processor = OpenCVSimulator(error_level, velocity_error, angular_instability)


""" Navigator """

navigator = Navigator(field, distance_calculator, motor_control, image_processor)
distance_calculator.navigator = navigator
image_processor.navigator = navigator
navigator.start()

""" Zeppelin """

name = "zilver"
zeppelin = Zeppelin(navigator,name)
zeppelin.start()

print "Simulator is up and running, baby."
                  
                                    
            
