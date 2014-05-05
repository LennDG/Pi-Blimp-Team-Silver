from Vector import Vector
from PID import PID
import threading
import time
import math

'''
This file contains the class Navigator.

@author: Rob
@Version: 1.0
'''



'''
    This class keeps track of the position and physical direction of the zeppelin.
    It also contains the map of the playfield and other useful information in
    regards to the position such as velocity, closest node etc.
'''
class Navigator(threading.Thread, object):
    
    MAXIMUM_SPEED = 20
    SLOW_DOWN_DISTANCE = 200
    ALLOWED_DEVIATION = 30

    '''
    This constructor initializes the object with a distance sensor and a control module for its motors.
    '''
    def __init__(self, field, distance_sensor, motor_control, image_processor):
        
        threading.Thread.__init__(self)
        
        # Initiate the motor control, distance sensor, image processor and height stabilizer.
        self.motor_control = motor_control
        self.distance_sensor = distance_sensor
        self.image_processor = image_processor
        
        # Initiate the field the navigator operates on.
        self.field = field
        
        # Initiate all the positional properties
        self.goal_reached = False
        self._goal_position = 0.0
        self.position = Vector(0,0)
        
        self.goal_height = 0.0
        
        # Construct a PID object to stabilize the zeppelin
        self.stabilizer = PID(self)
        
        self.angle = 0
        self.angular_velocity = 0 # Testing purposes only.
        
        self.velocity = Vector(0,0)
        
        self.last_updated = 0
        self.flying = False
        self.navigating = False
        
        
    @property    
    def height(self):
        return self.distance_sensor.height
    
    @property
    def goal_position(self):
        return self._goal_position
    
    @goal_position.setter
    def goal_position(self, position):
        self.goal_reached = False
        self._goal_position = position
    
    """
    This method starts the navigator thread and controls the position of the
    zeppelin.
    """
    def run(self):
        
        self.navigating = True
        
        while self.navigating:
            if self.goal_position == 0:
                time.sleep(0.1)
            else:
                if (self.goal_position - self.position).norm < Navigator.ALLOWED_DEVIATION:
                    self.goal_reached = True
                
                # Calculate the new position the zeppelin should be at, add some error
                
                # Dit gebeurt allemaal in die imagesimulator
                
                # Simulate the taking and decoding of a picture
                # will result in figure_images, zeppelin_image and time_stamp
                image_information = self.image_processor.generate_image()
                figure_images = image_information[0]
                zeppelin_image = image_information[1]
                time_stamp = image_information[2]
               
                result = self.field.locate_nodes(figure_images)
                
                if result == 0:
                    print "position detection failed"
                    # Turn the motors off
                    self.motor_control.left_motor.level = 0
                    self.motor_control.right_motor.level = 0
                    
                else:
                    self.update(result[0], result[1], result[2], result[3], zeppelin_image, time_stamp)
        
            
        
        
    """
    This method stops the navigator thread in a controlled way. Although I don't
    think it should be used.
    """    
    def stop(self):
        self.navigating = False
        
    
    """
    This method updates all the properties of the zeppelin, based on the supplied information.
    """
    def update(self, node_1, node_2, node_image_1, node_image_2, zeppelin_image, time):
        
        print node_1.figure.color, node_1.figure.shape, node_2.figure.color, node_2.figure.shape
        
        # Update the time properties
        time_lapsed = float(time - self.last_updated)
        self.last_updated = time
        
        # Put the given tuples in vector format and calculate the required vectors
#         node_image_1 = Vector(node_image_1[2], node_image_1[3])
#         node_image_2 = Vector(node_image_2[2], node_image_2[3])
        zeppelin_image = Vector(zeppelin_image[0], zeppelin_image[1])
        image_difference = node_image_2 - node_image_1
        node_difference = node_2.position - node_1.position
        
        # Calculating the angle properties
        new_angle = node_difference.angle - image_difference.angle
        print "angle: " + str(new_angle)
        self.angular_velocity = (new_angle - self.angle)/time_lapsed
        self.angle = new_angle + math.pi
        
        # Calculating positional properties.
        enlargement_factor = node_difference.norm/float(image_difference.norm)
        print "enlargement factor: " + str(enlargement_factor)
        relative_position = zeppelin_image - node_image_1
        relative_position = relative_position*enlargement_factor
        relative_position = relative_position.turn(new_angle)
        new_position = node_1.position + relative_position
        self.velocity = (new_position - self.position)/time_lapsed
        self.position = new_position
        print "current position: " + str(self.position.xcoord) + ", " + str(self.position.ycoord)
        print "current velocity: " + str(self.velocity.xcoord) + ", " + str(self.velocity.ycoord)
        
        self.update_motor_control()
    
    
    """
    This method calculates the velocity the zeppelin desires to reach its destination in a 
    straight as possible line.
    """    
    def calculate_goal_velocity(self):
        
        if self.goal_position == 0:
            return Vector(0,0)
        
        path = self.goal_position - self.position
        goal_velocity = 0
        
        if path.norm >= Navigator.SLOW_DOWN_DISTANCE:
            goal_velocity = Vector(Navigator.MAXIMUM_SPEED,0).turn(path.angle)
        else:
            goal_velocity = Vector(path.norm/Navigator.SLOW_DOWN_DISTANCE*Navigator.MAXIMUM_SPEED, 0).turn(path.angle)
            
        return goal_velocity
            
    
    """
    This method orders the motor control module to steer its motors as to obtain the
    goal velocity.
    """    
    def update_motor_control(self):
        
        goal_velocity = self.calculate_goal_velocity()
        
        velocity = goal_velocity - self.velocity
        print "velocity to be set: " + str(velocity.xcoord) + ", " + str(velocity.ycoord)
        
        scaling_factor = 100/Navigator.MAXIMUM_SPEED
        
        acceleration = Vector(velocity.xcoord*scaling_factor, velocity.ycoord*scaling_factor)
        
        print "acceleration: " + str(acceleration.xcoord) + ', ' + str(acceleration.ycoord)
        
        # The angle with which the zeppelin moves is the angle the acceleration makes with the x-axis
        # added to the angle the front of the zeppelin makes with the x-axis.
        self.motor_control.move(acceleration.angle - self.angle, acceleration.norm)
        print 'zeppelin angle: ' + str(self.angle)
    
  
    """
    This method calibrates the bias-parameter by starting the zeppelin on the ground and
    gradually increasing the vertical motor level untill it is able to lift the zeppelin off
    the ground.
    """
    def calibrate_bias(self):
        
        # Initialize the bias at 0
        bias = 0
        
        # While the height of the zeppelin does not exceed 6, the zeppelin is considered to
        # be on the ground and the level of the vertical motor is increased.
        while(not  self.current_height > 6):
            
            bias = bias + 1
            self.motor_control.vert_motor.level = bias
            
            # The distance sensor only supplies a new height every 0.6 seconds.
            time.sleep(0.6)
    
        # print out the result of the calibration
        print "The bias is calibrated at " + str(bias)
    
    

    #RAW methodes for testing purposes + protocol necessity
    def set_motor1(self,lvl):
        if(lvl >= -100 and lvl <= 100):
            self.motor_control.left_motor.level=lvl
    
    def set_motor2(self,lvl):
        if(lvl >= -100 and lvl <= 100):
            self.motor_control.right_motor.level=lvl
    
    def set_motor3(self,lvl):
        if(lvl >= -100 and lvl <= 100):
            self.motor_control.vert_motor.level=lvl
        
    
        